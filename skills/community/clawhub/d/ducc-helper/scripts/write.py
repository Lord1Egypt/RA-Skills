#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DUCC 配置写入脚本（增 / 改 / 删 / 发布）。

⚠ 安全约定（本 skill 采用「只有发布卡 --confirm」策略，与用户确认）：
  - set / update / delete：直接生效于「草稿」层（改的是待发布内容，未 release 前不影响线上运行）。
    这几个动作会立即执行，不需要 --confirm。
  - release（发布）：让草稿真正生效到线上运行实例，风险最高，必须加 --confirm 才下发；
    不加只预演（打印将要发布的 key、目标编排、批次计划）。

层级：命名空间(ns) → 配置文件(cfg) → profile(如 dev/common) → 配置项(item: key/value)
ns/cfg/prof 都可传 code 或数字 ID，自动解析（见 config.py）。

format：0=无格式(纯文本/字符串)，1=JSON（value 必须是合法 JSON 字符串）。

子命令：
  set     <ns> <cfg> <prof> <key> <value> [--format 0|1] [--desc ...]   新增或覆盖(存在则改)
  update  <ns> <cfg> <prof> <key> <value> [--format 0|1] [--desc ...]   仅修改已存在项
  delete  <ns> <cfg> <prof> <key>                                        删除配置项(草稿)
  release <ns> <cfg> <prof> <key> [<key> ...] --confirm                  发布(全量, 默认)
          [--orchestrate <code>]  指定灰度编排模板 code（见 orchestrates 子命令）
  orchestrates <ns>              列出可用的灰度发布编排模板

示例：
  python write.py set  pop_customs_center center_config common ducc.foo.switch true
  python write.py set  pop_customs_center center_config common ducc.foo.json '{"a":1}' --format 1
  python write.py delete pop_customs_center center_config common ducc.foo.switch
  python write.py release pop_customs_center center_config common ducc.foo.switch --confirm

【发布链路】(实测，全量路径)：
  POST  .../keys                      body=[key...]         预检/拿待发布项
  POST  .../submitAuditKeys           拿 taskId             建发布任务(可带 orchestrateCode)
  PUT   .../task/{taskId}/batch/0/releaseAction  {"action":"PRE_BATCH_SKIP"}  跳过灰度
  PUT   .../release/keys              body 带 configTaskId  执行, 返回新 version
灰度分批(逐批推进+轮询 batch/{n}/ips 全 COMPLETED)见 references/api.md「发布」节，脚本留 TODO。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import jme_auth  # noqa: E402
from ducc_client import DuccClient, add_common_args, emit, log  # noqa: E402


def _fail(msg, **extra):
    emit({"ok": False, "error": msg, **extra})
    sys.exit(1)


def _ctx(c, args, need_prof=True):
    """解析 ns/cfg/prof 三级并返回 id。发布/增删改都基于 profile。"""
    cfg_arg = getattr(args, "cfg", None)
    ns, cfg, prof = c.resolve_all(args.ns, cfg_arg, getattr(args, "prof", None), env=args.env)
    if not ns:
        _fail(f"命名空间未找到：{args.ns}")
    if cfg_arg is not None and not cfg:
        _fail(f"配置文件未找到：{cfg_arg}")
    if need_prof and not prof:
        hint = "（预发环境可能未开放）" if c.env == "pre" else ""
        _fail(f"profile 未找到：{args.prof}{hint}")
    return ns, cfg, prof


def _find_item(c, ns_id, cfg_id, prof_id, key, env):
    """在 profile 下按 key 精确查配置项，返回 item dict 或 None。"""
    _, data = c.get(
        f"/admin/v2/namespace/{ns_id}/config/{cfg_id}/profile/{prof_id}"
        f"/items/search?size=1000&page=1&fromRelease=false&orderField=updateTime&desc=desc",
        env=env)
    if not c.ok(data):
        return None
    for it in data.get("data", []):
        if it.get("key") == key:
            return it
    return None


def cmd_set(c, args):
    """新增或覆盖：存在则 update，不存在则 create。"""
    ns, cfg, prof = _ctx(c, args)
    base = f"/v1/namespace/{ns['id']}/config/{cfg['id']}/profile/{prof['id']}"
    existing = _find_item(c, ns['id'], cfg['id'], prof['id'], args.key, args.env)
    body = {"format": args.format, "value": args.value, "description": args.desc or ""}
    if existing:
        # 覆盖已有（PUT /item/{id}，body 不含 key）
        status, data = c.put(f"{base}/item/{existing['id']}", body, env=args.env)
        action = "updated"
    else:
        body_new = dict(body); body_new["key"] = args.key
        status, data = c.post(f"{base}/item", body_new, env=args.env)
        action = "created"
    if not c.ok(data):
        _fail(f"{action} 失败", status=status, raw=data)
    item = data.get("data", {})
    emit({"ok": True, "action": action, "env": c.env,
          "namespace": ns.get("code"), "config": cfg.get("code"), "profile": prof.get("code"),
          "key": args.key, "itemId": item.get("id"), "value": args.value, "format": args.format,
          "note": "已写入草稿；需 release 才生效到线上"})


def cmd_update(c, args):
    """仅修改已存在项（不存在报错）。"""
    ns, cfg, prof = _ctx(c, args)
    existing = _find_item(c, ns['id'], cfg['id'], prof['id'], args.key, args.env)
    if not existing:
        _fail(f"配置项不存在，无法 update：{args.key}（如需新增用 set）")
    base = f"/v1/namespace/{ns['id']}/config/{cfg['id']}/profile/{prof['id']}"
    body = {"format": args.format, "value": args.value, "description": args.desc or existing.get("description", "")}
    status, data = c.put(f"{base}/item/{existing['id']}", body, env=args.env)
    if not c.ok(data):
        _fail("update 失败", status=status, raw=data)
    emit({"ok": True, "action": "updated", "env": c.env,
          "namespace": ns.get("code"), "config": cfg.get("code"), "profile": prof.get("code"),
          "key": args.key, "itemId": existing['id'], "value": args.value, "format": args.format,
          "note": "已写入草稿；需 release 才生效到线上"})


def cmd_delete(c, args):
    ns, cfg, prof = _ctx(c, args)
    existing = _find_item(c, ns['id'], cfg['id'], prof['id'], args.key, args.env)
    if not existing:
        _fail(f"配置项不存在，无法删除：{args.key}")
    base = f"/v1/namespace/{ns['id']}/config/{cfg['id']}/profile/{prof['id']}"
    status, data = c.delete(f"{base}/item/{existing['id']}", env=args.env)
    if not c.ok(data):
        _fail("删除失败", status=status, raw=data)
    emit({"ok": True, "action": "deleted", "env": c.env,
          "namespace": ns.get("code"), "config": cfg.get("code"), "profile": prof.get("code"),
          "key": args.key, "itemId": existing['id'],
          "note": "已从草稿删除；需 release 才在线上生效删除"})


def cmd_orchestrates(c, args):
    """列出灰度发布编排模板。"""
    ns, _, _ = _ctx(c, args, need_prof=False)
    _, data = c.get(f"/v2/namespace/{ns['id']}/task_orchestrates?size=100&orderField=updateTime&desc=desc",
                    env=args.env)
    if not c.ok(data):
        _fail("编排模板列表获取失败", raw=data)
    out = []
    for t in data.get("data", []):
        batches = (t.get("template") or {}).get("batches", [])
        out.append({"code": t.get("code"), "name": t.get("name"), "batchCount": t.get("batchCount"),
                    "batches": [{"batchNum": b.get("batchNum"), "ipsPercentage": b.get("ipsPercentage")} for b in batches]})
    emit({"ok": True, "note": "全量发布不需要模板；灰度发布用 --orchestrate <code>",
          "count": len(out), "orchestrates": out})


def _version_name():
    """版本名 v+yyyyMMddHHmmss。DUCC 页面就是这个格式。"""
    import time
    return "v" + time.strftime("%Y%m%d%H%M%S")


def _orchestrate_detail(c, ns_id, code, env):
    """按 code 取编排模板详情（含 batches：每批 ipsPercentage）。用于灰度发布计划展示。"""
    _, data = c.get(f"/v2/namespace/{ns_id}/task_orchestrates?size=100&orderField=updateTime&desc=desc",
                    env=env)
    if not c.ok(data):
        return None
    for t in data.get("data", []):
        if t.get("code") == code:
            return {"code": code, "name": t.get("name"),
                    "batches": (t.get("template") or {}).get("batches", [])}
    return None


def cmd_release(c, args):
    ns, cfg, prof = _ctx(c, args)
    base_admin = f"/admin/v1/namespace/{ns['id']}/config/{cfg['id']}/profile/{prof['id']}"
    base_v1 = f"/v1/namespace/{ns['id']}/config/{cfg['id']}/profile/{prof['id']}"
    keys = args.keys
    erp = c.current_erp() or args.submitter
    if not erp:
        _fail("无法获取当前用户 erp（submitter），可用 --submitter 指定")

    gray = bool(args.orchestrate)
    plan = {
        "env": c.env, "namespace": ns.get("code"), "config": cfg.get("code"), "profile": prof.get("code"),
        "keys": keys, "submitter": erp,
        "mode": "灰度分批" if gray else "全量",
        "orchestrate": args.orchestrate or "(全量,无编排)",
    }
    if gray:
        tmpl = _orchestrate_detail(c, ns['id'], args.orchestrate, args.env)
        plan["batches"] = tmpl.get("batches") if tmpl else "(未知)"

    # ── 预演 ──
    if not args.confirm:
        emit({"ok": True, "dryRun": True, "plan": plan,
              "warning": "这是预演。发布会让草稿真正生效到线上运行实例。确认无误后加 --confirm 执行。"})
        return

    if gray:
        _release_gray(c, args, ns, cfg, prof, keys, erp, base_admin, base_v1)
    else:
        _release_full(c, args, ns, cfg, prof, keys, erp, base_admin, base_v1)


def _release_full(c, args, ns, cfg, prof, keys, erp, base_admin, base_v1):
    """全量发布（两步，无编排、无 PRE_BATCH_SKIP、一次 release/keys 走完）。"""
    ver = _version_name()
    # 1) 预检 keys（两个预检接口，页面都调，稳妥起见都发）
    c.post(f"{base_admin}/keys?hasInnerKey=true&workflowId=-1", keys, env=args.env)
    c.post(f"{base_admin}/item_releases/keys?hasInnerKey=true&workflowId=-1", keys, env=args.env)
    # 2) 建发布任务（全量：不带 orchestrateCode / batchInterval）
    submit_body = {"pushType": 0, "keys": keys, "submitter": erp, "description": args.desc or "",
                   "name": ver, "appendPreBatch": True}
    status, data = c.post(f"{base_admin}/submitAuditKeys", submit_body, env=args.env)
    if not c.ok(data):
        _fail("建发布任务(submitAuditKeys)失败", status=status, raw=data)
    task_id = data.get("data", {}).get("taskId")
    if not task_id:
        _fail("submitAuditKeys 未返回 taskId", raw=data)
    # 3) 执行发布（全量：不带 orchestrateCode）
    rel_body = {"pushType": 0, "submitter": erp, "description": args.desc or "",
                "configTaskId": task_id, "versionName": ver}
    status, data = c.put(f"{base_v1}/release/keys", rel_body, env=args.env)
    if not c.ok(data):
        _fail("执行发布(release/keys)失败", status=status, raw=data, taskId=task_id)
    emit({"ok": True, "action": "released", "mode": "全量", "env": c.env,
          "namespace": ns.get("code"), "config": cfg.get("code"), "profile": prof.get("code"),
          "keys": keys, "taskId": task_id, "versionName": ver,
          "newVersion": data.get("data", {}).get("version")})


def _release_gray(c, args, ns, cfg, prof, keys, erp, base_admin, base_v1):
    """灰度分批发布：建任务(带模板码) → PRE_BATCH_SKIP → 逐批 release/keys，
    每批之间轮询 batch/{n}/ips 等全 COMPLETED 再发下一批（用户强调的核心安全逻辑）。"""
    import time
    ver = _version_name()
    # 1) 预检
    c.post(f"{base_admin}/keys?hasInnerKey=true&workflowId=-1", keys, env=args.env)
    c.post(f"{base_admin}/item_releases/keys?hasInnerKey=true&workflowId=-1", keys, env=args.env)
    # 2) 建任务（带模板码）
    submit_body = {"pushType": 0, "keys": keys, "submitter": erp, "description": args.desc or "",
                   "orchestrateCode": args.orchestrate, "batchInterval": 0, "name": ver, "appendPreBatch": True}
    status, data = c.post(f"{base_admin}/submitAuditKeys", submit_body, env=args.env)
    if not c.ok(data):
        _fail("建发布任务(submitAuditKeys)失败", status=status, raw=data)
    task_id = data.get("data", {}).get("taskId")
    if not task_id:
        _fail("submitAuditKeys 未返回 taskId", raw=data)
    # 3) PRE_BATCH_SKIP 跳过预批次（batch 0 是 appendPreBatch 加的预批次）
    c.put(f"{base_admin}/task/{task_id}/batch/0/releaseAction", {"action": "PRE_BATCH_SKIP"}, env=args.env)
    # 4) 逐批推进。语义（实测）：task.batchNum 指向"下一个待发批"，
    #    每次 release/keys 发布当前 batchNum 指向的那一批，发完 batchNum++。
    #    所以：release 前记 n=batchNum → release → 轮询 batch n 的 ips 全 COMPLETED → 再发下一批。
    rel_body = {"pushType": 0, "submitter": erp, "description": args.desc or "",
                "orchestrateCode": 1, "batchInterval": 0, "configTaskId": task_id, "versionName": ver}
    batches_done = []
    import time
    for step in range(20):  # 批次数上限保护
        _, td = c.get(f"{base_v1}/task/{task_id}", env=args.env)
        d = td.get("data") or {}
        if d.get("status") == -2:  # 任务已结束
            break
        n = d.get("batchNum", 0)          # 本次将发布的批号
        batch_count = d.get("batchCount", 0)
        # 推进：发布第 n 批
        status, data = c.put(f"{base_v1}/release/keys", rel_body, env=args.env)
        if not c.ok(data):
            _fail("灰度发布推进(release/keys)失败", status=status, raw=data, taskId=task_id,
                  done=batches_done)
        time.sleep(2)
        # 轮询第 n 批 IP 全 COMPLETED（用户强调：等前批 IP 都成功再发下一批）
        ok_batch = _wait_batch_complete(c, base_v1, task_id, n, args.env, timeout=180)
        batches_done.append({"batch": n, "allCompleted": ok_batch})
        if not ok_batch:
            _fail(f"第 {n} 批 IP 未全部 COMPLETED（超时），已暂停，不再发下一批",
                  taskId=task_id, done=batches_done,
                  hint="去页面确认该批 IP 状态；修复后可在页面继续或重发")
        # 是否发完：再查 task 是否结束
        _, td2 = c.get(f"{base_v1}/task/{task_id}", env=args.env)
        if (td2.get("data") or {}).get("status") == -2:
            break
        if args.batch_pause:
            log(f"第 {n} 批已全部 COMPLETED，按 --batch-pause 暂停，未发下一批。")
            break
    # 最终状态
    _, td = c.get(f"{base_v1}/task/{task_id}", env=args.env)
    d = td.get("data") or {}
    emit({"ok": True, "action": "released", "mode": "灰度分批", "env": c.env,
          "namespace": ns.get("code"), "config": cfg.get("code"), "profile": prof.get("code"),
          "keys": keys, "taskId": task_id, "versionName": ver,
          "finalStatus": d.get("status"), "finalBatch": d.get("batchNum"), "batchCount": d.get("batchCount"),
          "batchesDone": batches_done,
          "note": "status=-2 表示已全部发布完成" if d.get("status") == -2 else "未走完，去页面确认剩余批次"})


def _wait_batch_complete(c, base_v1, task_id, batch_num, env, timeout=120):
    """轮询某批的 IP 状态，全部 COMPLETED 返回 True；超时/有失败返回 False。"""
    import time
    deadline = timeout
    waited = 0
    while waited < deadline:
        _, data = c.get(f"{base_v1}/task/{task_id}/batch/{batch_num}/ips", env=env)
        if c.ok(data):
            result = (data.get("data") or {}).get("result", [])
            if result:
                statuses = [x.get("status") for x in result]
                if all(s == "COMPLETED" for s in statuses):
                    return True
                if any(s in ("FAILED", "ERROR") for s in statuses):
                    return False
        time.sleep(3)
        waited += 3
    return False


def main():
    ap = argparse.ArgumentParser(description="DUCC 配置写入（增/改/删/发布）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    for name, help_ in [("set", "新增或覆盖配置项"), ("update", "仅修改已存在项")]:
        p = sub.add_parser(name, help=help_)
        p.add_argument("ns"); p.add_argument("cfg"); p.add_argument("prof")
        p.add_argument("key"); p.add_argument("value")
        p.add_argument("--format", type=int, choices=[0, 1], default=0, help="0=无格式(默认) 1=JSON")
        p.add_argument("--desc", default="", help="配置项描述")
        add_common_args(p)
        p.set_defaults(func=cmd_set if name == "set" else cmd_update)

    p = sub.add_parser("delete", help="删除配置项（草稿）")
    p.add_argument("ns"); p.add_argument("cfg"); p.add_argument("prof"); p.add_argument("key")
    add_common_args(p)
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("orchestrates", help="列出灰度发布编排模板")
    p.add_argument("ns")
    add_common_args(p)
    p.set_defaults(func=cmd_orchestrates)

    p = sub.add_parser("release", help="发布配置项（默认全量；只有加 --confirm 才真下发）")
    p.add_argument("ns"); p.add_argument("cfg"); p.add_argument("prof")
    p.add_argument("keys", nargs="+", help="要发布的一个或多个 key")
    p.add_argument("--confirm", action="store_true", help="真正执行发布（不加只预演）")
    p.add_argument("--orchestrate", default="", help="灰度编排模板 code（见 orchestrates 子命令）；不填=全量")
    p.add_argument("--batch-pause", action="store_true",
                   help="灰度发布时只发一批就暂停（发完当前批+等IP全COMPLETED后停），便于人工确认再继续")
    p.add_argument("--submitter", default="", help="发布人 erp（默认取当前登录用户）")
    p.add_argument("--desc", default="", help="发布描述")
    add_common_args(p)
    p.set_defaults(func=cmd_release)

    args = ap.parse_args()
    if getattr(args, "clear_cache", False):
        jme_auth.clear_cache(); print("token 缓存已清除"); return
    c = DuccClient(env=getattr(args, "env", "online"),
                   force_refresh=getattr(args, "force_refresh", False))
    args.func(c, args)


if __name__ == "__main__":
    main()
