"""app.py — BizyAir 远端对象 CLI 入口。

所有真正"打 BizyAir API" 的 CLI 都在这。dispatch.py 只是个 wrapper，本质是
shell 到这里。

入口分类：
  --check / --wallet                       账号验证 + 余额
  --browse / --search                      列表 / 关键词搜索
  --pick-image-candidates / --pick-video-... 模型挑候选（提供给 LLM 选）
  --info / --info-from-link                远端对象元数据 + contract（debug 全集 /
                                            默认精简，见 _strip_info_debug_payload）
  --prefill-card <link-or-id>              生成预填卡（统一渲染器，菜单 10 个固定模型和远端任意 app 都用这个）
  --run <app-id>                           真正提交执行（创建任务、轮询、下载）

api.py / remote.py / contract.py 是 app.py 的肌肉；本文件主要做 CLI 解析 + 路由。
"""
from __future__ import annotations
import argparse, json, re, sys
from typing import Any

import api
import contract
import remote
import search
import common
from common import API_BASE, WEBAPP_RETRY_LIMIT, build_prompt_bundle_for_args

def cmd_check(api_key_arg: str | None):
    key = api.resolve_api_key(api_key_arg)
    if not key:
        print(json.dumps({'status': 'no_key', 'message': 'No BizyAir API key configured', 'supported_inputs': {'cli': '--api-key YOUR_BIZYAIR_KEY', 'env': 'BIZYAIR_API_KEY', 'config': f'{common.config_display_path()} -> credentials.api_key'}, 'recommended': f'Save the key to {common.config_display_path()} at credentials.api_key'}, ensure_ascii=False))
        return
    # 真打一次 BizyAir 钱包 API 验证 key 有效性。
    # 不靠占位符字符串匹配（否则换个文案就漏过），靠服务器自己回应。
    resp = api.request_json('GET', f'{API_BASE}/y/v1/wallet', key)
    http_status = (resp or {}).get('status')
    if api.result_is_ok(resp):
        # 成功 envelope: {ok: True, status: 200, data: {code: 20000, data: {wallet}}}
        inner = resp.get('data') if isinstance(resp, dict) else {}
        biz_code = inner.get('code') if isinstance(inner, dict) else None
        if biz_code != 20000:
            print(json.dumps({'status': 'invalid_key', 'key_prefix': key[:4] + '****', 'source': api.get_key_source(api_key_arg), 'message': 'API key 无效或已失效，请检查后重新配置', 'http_status': http_status, 'server_code': biz_code}, ensure_ascii=False))
            return
        data = api.extract_result_data(resp)
        total_amount = data.get('total_balance_amount')
        if isinstance(total_amount, (int, float)) and total_amount <= 0:
            print(json.dumps({'status': 'no_balance', 'key_prefix': key[:4] + '****', 'source': api.get_key_source(api_key_arg), 'message': 'API key 有效但余额为 0，请先充值再使用'}, ensure_ascii=False))
            return
        print(json.dumps({'status': 'ok', 'key_prefix': key[:4] + '****', 'source': api.get_key_source(api_key_arg)}, ensure_ascii=False))
        return
    # 鉴权失败 / 占位符 / 假 key：safe_request_json 会返回 {ok: False, status: 401, error: {...}}
    print(json.dumps({'status': 'invalid_key', 'key_prefix': key[:4] + '****', 'source': api.get_key_source(api_key_arg), 'message': 'API key 无效或已失效，请检查后重新配置', 'http_status': http_status}, ensure_ascii=False))

def cmd_wallet(api_key_arg: str | None):
    api_key = api.require_api_key(api_key_arg)
    resp = api.request_json('GET', f'{API_BASE}/y/v1/wallet', api_key)
    source = api.get_key_source(api_key_arg)
    data = api.extract_result_data(resp) if isinstance(resp, dict) else {}
    total_amount = data.get('total_balance_amount')
    if isinstance(total_amount, (int, float)):
        if total_amount >= 50000:
            verdict = '很充足，放心造，火力相当猛～'
        elif total_amount >= 10000:
            verdict = '还挺够用，正常跑一阵子问题不大～'
        elif total_amount >= 3000:
            verdict = '还能顶一会儿，但别太浪，记得盯着点余额。'
        else:
            verdict = '有点偏紧了，建议尽快补一点，免得跑到一半掉链子。'
    else:
        verdict = '余额拿到了，但我建议你还是顺手盯一下，别真跑空。'
    print(json.dumps({'status': 'ok', 'source': source, 'wallet': {'charge_balance': data.get('charge_balance'), 'gift_balance': data.get('gift_balance'), 'total_balance': data.get('total_balance'), 'charge_balance_amount': data.get('charge_balance_amount'), 'gift_balance_amount': data.get('gift_balance_amount'), 'total_balance_amount': data.get('total_balance_amount')}, 'summary': f"当前总余额 {data.get('total_balance')}（充值 {data.get('charge_balance')}，赠送 {data.get('gift_balance')}）", 'verdict': verdict, 'raw': resp}, ensure_ascii=False, indent=2))

def cmd_browse(modality: str | None=None, stability: str | None=None, *, api_key_arg: str | None=None, remote_source: str='community', page: int=1, page_size: int=10, base_models: str | None=None):
    api_key = api.require_api_key(api_key_arg)
    remote_module = globals()['remote']
    model_types = remote_module.normalize_remote_type(modality)
    sort = 'Auto' if common.normalized_text(remote_source) == 'official' else 'Recently'
    resp = api.fetch_remote_models(api_key, remote_source=remote_source, page=page, page_size=page_size, keyword='', sort=sort, model_types=model_types, base_models=base_models)
    print(json.dumps({'source': 'remote', 'remote_source': remote_source, 'query': {'page': page, 'page_size': page_size, 'model_types': model_types, 'base_models': base_models, 'sort': sort}, 'result': resp}, ensure_ascii=False, indent=2))

def cmd_search(query: str, *, api_key_arg: str | None=None, remote_source: str='community', page: int=1, page_size: int=10, modality: str | None=None, sort: str | None=None, base_models: str | None=None):
    api_key = api.require_api_key(api_key_arg)
    remote_module = globals()['remote']
    semantic_plan = search.build_semantic_plan(query, modality)
    model_types = remote_module.normalize_remote_type(modality)
    resolved_sort = sort or ('Auto' if common.normalized_text(remote_source) == 'official' else 'Recently')
    primary_keyword = (semantic_plan.get('search_queries') or [query])[0]
    resp = api.fetch_remote_models(api_key, remote_source=remote_source, page=page, page_size=page_size, keyword=primary_keyword, sort=resolved_sort, model_types=model_types, base_models=base_models)
    items = api.extract_result_data(resp).get('list', []) if isinstance(resp, dict) else []
    platform_results = search.format_remote_candidates(items, semantic_plan, common.normalized_text(modality) if modality else None)
    print(json.dumps({'source': 'remote', 'remote_source': remote_source, 'query': {'keyword': primary_keyword, 'page': page, 'page_size': page_size, 'model_types': model_types, 'base_models': base_models, 'sort': resolved_sort}, 'semantic_plan': semantic_plan, 'platform_results': platform_results, 'candidates': platform_results, 'result': resp}, ensure_ascii=False, indent=2))

def cmd_info(app_id: str, *, remote: bool=False, api_key_arg: str | None=None, include_workflow: bool=False):
    # 注意：参数名 `remote` 会遮蔽顶部 import 的 `remote` 模块，
    # 直接 `remote.build_remote_info_output(...)` 会报 AttributeError。
    # 这里通过 globals() 显式取模块，避免 shadow。
    if remote:
        remote_module = globals()['remote']
        out = remote_module.build_remote_info_output(app_id, api_key_arg=api_key_arg, include_workflow=include_workflow)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

def cmd_info_from_link(target: str, *, api_key_arg: str | None=None, include_workflow: bool=True, debug: bool=False):
    """`--info-from-link X`。打印远端对象的完整 info JSON。
    debug=False（默认）：去掉 result.raw 分支 + 所有 fields[].raw_node 子节点
    （内部 fields[].field_value 已含原始值），输出能砍掉 ~60% 字节。
    debug=True：保留全部，给开发调试用。
    cmd_prefill_card 内部也用 build_remote_info_output，但走 in-process 不走 stdout，
    所以不受这里 strip 影响。
    """
    resolved = remote.resolve_info_target(target)
    if not resolved.get('ok'):
        print(json.dumps(resolved, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)
    if resolved.get('input_kind') == 'workflow_link':
        print(json.dumps({'error': 'WORKFLOW_LINK_NOT_SUPPORTED', 'input_kind': 'workflow_link', 'input_value': resolved.get('input_value'), 'draft_id': resolved.get('resolved_object_id'), 'message': common.WORKFLOW_LINK_NOT_SUPPORTED_MESSAGE}, ensure_ascii=False, indent=2))
        return
    api_key = api.resolve_api_key(api_key_arg)
    original_object_id = str(resolved['resolved_object_id'])
    final_object_id = original_object_id
    out = remote.build_remote_info_output(final_object_id, api_key_arg=api_key_arg, include_workflow=include_workflow)
    out_for_print = out if debug else _strip_info_debug_payload(out)
    print(json.dumps({'source': 'remote-info-from-link', 'input_kind': resolved.get('input_kind'), 'input_value': resolved.get('input_value'), 'normalized_url': resolved.get('normalized_url'), 'original_object_id': original_object_id, 'resolved_object_id': final_object_id, 'result': out_for_print}, ensure_ascii=False, indent=2))


def _strip_info_debug_payload(out: dict[str, Any]) -> dict[str, Any]:
    """Return a deep-copied view of build_remote_info_output() with raw branch / raw_node trimmed.

    - Drops top-level `out['raw']` (debug-only branch; ~50% of bytes).
    - Recursively drops every `raw_node` key inside `summary` (each contract field
      currently carries a self-duplicating raw_node copy; appears under both
      `summary.resolved_contract.fields[]` and `summary.executable_draft.resolved_contract.fields[]`).

    Caller-side cosmetic stripping only — does not mutate the original `out`,
    so other consumers (cmd_prefill_card) keep getting the full structure.
    """
    if not isinstance(out, dict):
        return out

    def _scrub(node: Any) -> Any:
        if isinstance(node, dict):
            return {k: _scrub(v) for k, v in node.items() if k != 'raw_node'}
        if isinstance(node, list):
            return [_scrub(v) for v in node]
        return node

    trimmed = {k: v for k, v in out.items() if k != 'raw'}
    summary = trimmed.get('summary')
    if isinstance(summary, dict):
        trimmed['summary'] = _scrub(summary)
    return trimmed

def cmd_prefill_card(target: str, args: argparse.Namespace):
    target_info = remote.resolve_remote_prefill_target(target, api_key_arg=args.api_key)
    if not target_info.get('ok'):
        print(json.dumps(target_info, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)
    out = remote.build_remote_info_output(str(target_info['resolved_object_id']), api_key_arg=args.api_key, include_workflow=True)
    summary = out.get('summary') or {}
    raw = out.get('raw') or {}
    execution_target = raw.get('execution_target') or {}
    webapp_detail_data = execution_target.get('webapp_detail') or raw.get('webapp_detail') or {}
    if isinstance(webapp_detail_data, dict) and isinstance(webapp_detail_data.get('data'), dict):
        webapp_detail_data = webapp_detail_data.get('data', {})
    print(remote.build_remote_prefilled_card(summary, args, input_kind=target_info.get('input_kind'), original_object_id=target_info.get('original_object_id'), resolved_object_id=target_info.get('resolved_object_id'), draft_resolution=target_info.get('draft_resolution'), webapp_detail_data=webapp_detail_data))
    return

def cmd_run(args: argparse.Namespace):
    api_key = api.resolve_api_key(args.api_key)
    raw_app = str(args.app or '').strip()
    if raw_app.isdigit():
        if not api_key:
            print(json.dumps({'error': 'NO_REMOTE_CREDENTIAL', 'message': 'Remote app run preflight requires api key', 'supported_inputs': {'api_key': f'--api-key / BIZYAIR_API_KEY / {common.config_display_path()} -> credentials.api_key'}}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
        preflight = remote.preflight_remote_app_run(api_key, raw_app)
        id_diagnosis = api.diagnose_remote_numeric_id(api_key, raw_app)
        uploaded_urls = [api.upload_input_file(api_key, p) for p in args.image or []]
        uploaded_audios = [api.upload_input_file(api_key, p) for p in args.audio or []]
        uploaded_videos = [api.upload_input_file(api_key, p) for p in args.video or []]
        preflight_summary = remote.build_remote_info_summary(bizy_model_id=str(raw_app), detail_result=preflight.get('detail'), webapp_detail=preflight.get('webapp_detail'), fallback_model=None, version_detail=preflight.get('version_detail'), workflow=preflight.get('workflow'), execution_target=preflight.get('execution_target'), resolved_contract=preflight.get('resolved_contract'))
        execution_target = preflight.get('execution_target') or {}
        runtime_webapp = api.extract_result_data(execution_target.get('webapp_detail'))
        if not execution_target.get('supported'):
            print(json.dumps({'error': 'REMOTE_APP_RUN_NOT_SUPPORTED', 'message': raw_app, 'detail': execution_target.get('message') or '参数和说明都拿到了，但这个对象目前不支持直接代跑。建议你拿整理好的参数去网页端运行。', 'reason': execution_target.get('reason'), 'support_scope': execution_target.get('support_scope'), 'preflight': {'id_diagnosis': id_diagnosis, 'summary': preflight_summary}}, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(1)
        if not runtime_webapp.get('id'):
            print(json.dumps({'error': 'REMOTE_APP_RUN_NOT_SUPPORTED', 'message': raw_app, 'detail': '这个对象的参数和说明我已经拿到了，不过后台的执行通道还没完全接好。为了防止跑错，这轮我先不帮你提交运行啦，等路线通了咱们再来！', 'reason': 'missing_execution_webapp_id', 'preflight': {'id_diagnosis': id_diagnosis, 'summary': preflight_summary}}, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(1)
        missing_media = remote.summarize_missing_remote_media(preflight, args, uploaded_urls=uploaded_urls, uploaded_audios=uploaded_audios, uploaded_videos=uploaded_videos)
        if missing_media:
            print(json.dumps({'error': 'REMOTE_APP_RUN_REQUIRES_USER_MEDIA', 'message': raw_app, 'detail': '这个应用带有站内示例素材，但执行时必须换成你自己的素材，不能直接沿用站内素材。', 'reason': 'station_demo_media_must_be_replaced', 'missing_inputs': missing_media, 'classification': {'bucket': 'user_or_material', 'reason': 'missing_user_media', 'retryable': False}, 'preflight': {'id_diagnosis': id_diagnosis, 'summary': preflight_summary}}, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(1)
        final_attempt = None
        last_poll_result = None
        for retry_index in range(WEBAPP_RETRY_LIMIT + 1):
            attempt = api.create_remote_task_attempt(api_key, raw_app, preflight, args, uploaded_urls=uploaded_urls, uploaded_audios=uploaded_audios, uploaded_videos=uploaded_videos, use_async=not args.sync)
            final_attempt = attempt
            attempt_result = attempt.get('result') or {}
            nested_data = attempt_result.get('data', {}) if isinstance(attempt_result, dict) else {}
            if isinstance(nested_data, dict) and isinstance(nested_data.get('data'), dict):
                nested_data = nested_data.get('data', {})
            request_id = attempt_result.get('data', {}).get('requestId') or attempt_result.get('data', {}).get('request_id') or nested_data.get('requestId') or nested_data.get('request_id') or attempt_result.get('requestId') or attempt_result.get('request_id') if isinstance(attempt_result, dict) else None
            task_id = attempt_result.get('data', {}).get('task_id') or attempt_result.get('data', {}).get('taskId') or nested_data.get('task_id') or nested_data.get('taskId') or attempt_result.get('task_id') or attempt_result.get('taskId') if isinstance(attempt_result, dict) else None
            if request_id:
                print(f'REQUEST_ID:{request_id}')
                outputs_resp = api.poll_until_done(api_key, request_id)
                outputs = api.extract_result_data(outputs_resp).get('outputs', [])
                if not outputs:
                    print(json.dumps({'error': 'NO_OUTPUTS', 'detail': outputs_resp}, ensure_ascii=False), file=sys.stderr)
                    sys.exit(1)
                saved_paths = api.download_outputs(outputs, args.output)
                api.emit_downloaded_outputs(outputs, saved_paths)
                return
            if task_id:
                print(f'TASK_ID:{task_id}')
                task_status = attempt_result.get('data', {}).get('task_status') or nested_data.get('task_status') or attempt_result.get('task_status')
                if task_status:
                    print(f'TASK_STATUS:{task_status}')
                ws_url = attempt_result.get('data', {}).get('ws_url') or nested_data.get('ws_url') or attempt_result.get('ws_url')
                if ws_url:
                    print(f'WS_URL:{ws_url}')
                return
            break
        print(json.dumps({'error': 'REMOTE_APP_RUN_ATTEMPT_FAILED', 'message': raw_app, 'detail': 'Remote app submit was attempted with currently confirmed fields. Service response attached for next payload alignment.', 'attempt': final_attempt, 'last_poll_result': last_poll_result, 'preflight': {'auth_mode': 'api_key_only', 'bizy_model_id': preflight.get('bizy_model_id'), 'version_id': preflight.get('version_id'), 'detail_ok': api.result_is_ok(preflight.get('detail')), 'webapp_detail_ok': api.result_is_ok(preflight.get('webapp_detail')), 'version_detail_ok': api.result_is_ok(preflight.get('version_detail')), 'workflow_ok': api.result_is_ok(preflight.get('workflow')), 'id_diagnosis': id_diagnosis, 'summary': preflight_summary, 'detail': api.unwrap_result_payload(preflight.get('detail')), 'webapp_detail': api.unwrap_result_payload(preflight.get('webapp_detail')), 'version_detail': api.unwrap_result_payload(preflight.get('version_detail')), 'workflow': api.unwrap_result_payload(preflight.get('workflow'))}}, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='BizyAir curated AI app client')
    p.add_argument('--api-key')
    p.add_argument('--check', action='store_true')
    p.add_argument('--wallet', action='store_true')
    p.add_argument('--browse', action='store_true')
    p.add_argument('--search')
    p.add_argument('--pick-image-candidates')
    p.add_argument('--pick-video-candidates')
    p.add_argument('--modality')
    p.add_argument('--stability')
    p.add_argument('--info')
    p.add_argument('--info-from-link', help='Accept a BizyAir app/workflow link or raw numeric id and return remote info')
    p.add_argument('--prefill-card', help='Accept a BizyAir app/workflow link or raw numeric id and return a remote prefilled confirmation card')
    p.add_argument('--remote', action='store_true', help='Use API-key-backed remote discovery/detail')
    p.add_argument('--remote-source', choices=['community', 'official'], default='community')
    p.add_argument('--page', type=int, default=1)
    p.add_argument('--page-size', type=int, default=10)
    p.add_argument('--reply-format', choices=['json', 'markdown'], default='json')
    p.add_argument('--limit', type=int, default=10, help='Top-N candidates returned by --pick-image-candidates / --pick-video-candidates. Default 10. Use a smaller value (e.g. 3) for concise recommendations or a larger value (e.g. 20) when user asks to inventory all available models.')
    p.add_argument('--sort')
    p.add_argument('--base-models')
    p.add_argument('--with-workflow', action='store_true', help='When used with --info --remote, also resolve the first version workflow JSON')
    p.add_argument('--run', dest='app')
    p.add_argument('--prompt')
    p.add_argument('--image', action='append')
    p.add_argument('--audio', action='append')
    p.add_argument('--video', action='append')
    p.add_argument('--aspect-ratio')
    p.add_argument('--resolution')
    p.add_argument('--steps', type=int)
    p.add_argument('--duration', type=int)
    p.add_argument('--seed', type=int)
    p.add_argument('--random-seed', action='store_true')
    p.add_argument('--model-name')
    p.add_argument('--width', type=int)
    p.add_argument('--height', type=int)
    p.add_argument('--param', action='append', help='Extra raw input_values override: key=value')
    p.add_argument('-o', '--output')
    p.add_argument('--sync', action='store_true', help='Use sync mode instead of async polling mode')
    p.add_argument('--debug', action='store_true', help='Include the raw debug branch in --info-from-link / --info output')
    return p

def main():
    args = build_parser().parse_args()
    if args.check:
        cmd_check(args.api_key)
        return
    if args.wallet:
        cmd_wallet(args.api_key)
        return
    if args.browse:
        cmd_browse(args.modality, args.stability, api_key_arg=args.api_key, remote_source=args.remote_source, page=args.page, page_size=args.page_size, base_models=args.base_models)
        return
    if args.search:
        cmd_search(args.search, api_key_arg=args.api_key, remote_source=args.remote_source, page=args.page, page_size=args.page_size, modality=args.modality, sort=args.sort, base_models=args.base_models)
        return
    if args.pick_image_candidates:
        search.cmd_pick_image_candidates(args.pick_image_candidates, api_key_arg=args.api_key, remote_source=args.remote_source, page=args.page, page_size=args.page_size, sort=args.sort, base_models=args.base_models, limit=args.limit, reply_format=args.reply_format)
        return
    if args.pick_video_candidates:
        search.cmd_pick_video_candidates(args.pick_video_candidates, api_key_arg=args.api_key, remote_source=args.remote_source, page=args.page, page_size=args.page_size, sort=args.sort, base_models=args.base_models, limit=args.limit, reply_format=args.reply_format)
        return
    if args.info_from_link:
        cmd_info_from_link(args.info_from_link, api_key_arg=args.api_key, include_workflow=True, debug=bool(getattr(args, 'debug', False)))
        return
    if args.prefill_card:
        cmd_prefill_card(args.prefill_card, args)
        return
    if args.info:
        cmd_info(args.info, remote=args.remote, api_key_arg=args.api_key, include_workflow=args.with_workflow)
        return
    if args.app:
        cmd_run(args)
        return
    build_parser().print_help()

if __name__ == "__main__":
    main()
