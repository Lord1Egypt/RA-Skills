# -*- coding: utf-8 -*-

import difflib
import json
import re
import time
from datetime import datetime
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR.parent / "assets" / "config.json"


def load_config():
    with open(str(CONFIG_PATH), "r", encoding="utf-8") as f:
        return json.load(f)


def get_jenkins_cfg(cfg):
    jk = cfg.get("jenkins")
    if not jk or not jk.get("url"):
        return None
    return jk


def get_jenkins_job_name(cfg, repo_name, job_type="ci", env=None):
    jk = cfg.get("jenkins", {})
    repo_info = cfg.get("repos", {}).get(repo_name, {})
    github_repo = repo_info.get("repo", repo_name)
    cd_mode = jk.get("cd_trigger_mode", "auto_cd_param")
    if job_type == "cd":
        override = repo_info.get("jenkins_cd")
        if override:
            return override
        if cd_mode == "separate_job":
            env_job_map = jk.get("cd_job_by_env", {}) or {}
            if env and env_job_map.get(env):
                return env_job_map[env]
            common_job = jk.get("cd_job_name")
            if common_job:
                return common_job
        template = jk.get("cd_job_template", "{repo}-deploy")
    else:
        override = repo_info.get("jenkins_ci")
        template = jk.get("ci_job_template", "{repo}-build")
    return override or template.format(repo=github_repo, env=env or "")


def normalize_repo_key(value):
    return str(value or "").strip().lower().replace("_", "-")


def resolve_repos(cfg, names):
    all_repos = cfg.get("repos", {})
    aliases = cfg.get("service_aliases", {}) or {}
    normalized_repo_names = {
        normalize_repo_key(repo_name): repo_name for repo_name in all_repos.keys()
    }
    normalized_aliases = {
        normalize_repo_key(alias): target for alias, target in aliases.items()
    }

    selected = []
    for raw_name in names:
        name = str(raw_name or "").strip()
        normalized = normalize_repo_key(name)
        if not normalized:
            continue

        alias_target = normalized_aliases.get(normalized)
        if alias_target and alias_target in all_repos:
            selected.append(alias_target)
            continue

        exact_match = normalized_repo_names.get(normalized)
        if exact_match:
            selected.append(exact_match)
            continue

        matches = [
            repo_name
            for repo_name in all_repos.keys()
            if normalized in normalize_repo_key(repo_name)
        ]
        if len(matches) == 1:
            selected.append(matches[0])

    result = []
    seen = set()
    for repo_name in selected:
        if repo_name in seen:
            continue
        seen.add(repo_name)
        info = all_repos[repo_name]
        result.append((repo_name, info.get("dir", repo_name), info.get("repo", repo_name)))
    return result


def _normalize_branch(branch, prefix):
    if not branch:
        return None
    return branch if branch.startswith(prefix) else "{}{}".format(prefix, branch)


def _extract_parameters(actions):
    params = {}
    for action in actions or []:
        for item in action.get("parameters") or []:
            name = item.get("name")
            if name:
                params[name] = item.get("value")
    return params


def _jenkins_get(url, user, api_token, timeout=15):
    resp = requests.get(url, auth=(user, api_token), timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _build_jenkins_params(cfg, repo_name, job_type="ci", branch=None):
    jk = cfg.get("jenkins", {})
    repo_info = cfg.get("repos", {}).get(repo_name, {})
    github_repo = repo_info.get("repo", repo_name)
    cd_mode = jk.get("cd_trigger_mode", "auto_cd_param")

    if job_type == "cd" and cd_mode == "separate_job":
        projects_param = jk.get("cd_projects_param", "PROJECTS")
        project_name = repo_info.get("cd_project") or github_repo
        params = {projects_param: project_name}
        for key, value in (jk.get("cd_static_params") or {}).items():
            if value is not None:
                params[str(key)] = str(value)
        return params

    branch_param = jk.get("branch_param", "GIT_BRANCH")
    branch_prefix = jk.get("branch_prefix", "origin/")
    cd_param = jk.get("cd_param", "AUTO_CD")
    branch_val = _normalize_branch(branch, branch_prefix)
    params = {}
    if branch_val:
        params[branch_param] = branch_val
    params[cd_param] = "True" if job_type == "cd" else "False"
    return params


def _normalize_param_value(value):
    if value is None:
        return ""
    text = str(value).strip()
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered
    return text


def _params_match(actual, expected):
    for key, value in expected.items():
        if _normalize_param_value(actual.get(key)) != _normalize_param_value(value):
            return False
    return True


def _find_duplicate_queue_item(base_url, user, api_token, job_url, expected_params):
    queue_api = "{}/queue/api/json?tree=items[id,url,task[name,url],params,cancelled,why,executable[url],actions[parameters[name,value]]]".format(base_url)
    data = _jenkins_get(queue_api, user, api_token)
    for item in data.get("items") or []:
        if item.get("cancelled"):
            continue
        task = item.get("task") or {}
        if task.get("url") != job_url:
            continue
        params = _extract_parameters(item.get("actions"))
        if not params and item.get("params"):
            raw = str(item.get("params"))
            for line in raw.splitlines():
                if "=" in line:
                    k, v = line.split("=", 1)
                    params[k.strip()] = v.strip()
        if _params_match(params, expected_params):
            return {
                "kind": "queue",
                "queue_url": item.get("url"),
                "build_url": ((item.get("executable") or {}).get("url")),
                "params": params,
            }
    return None


def _find_duplicate_running_build(base_url, user, api_token, job_path, expected_params):
    job_api = "{}/job/{}/api/json?tree=builds[url,number,building,actions[parameters[name,value]]]{},lastBuild[url,number,building,actions[parameters[name,value]]]".format(
        base_url, job_path, ""
    )
    data = _jenkins_get(job_api, user, api_token)
    candidates = []
    builds = data.get("builds") or []
    last_build = data.get("lastBuild")
    if last_build:
        builds = [last_build] + builds
    seen = set()
    for build in builds:
        url = build.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        if not build.get("building"):
            continue
        params = _extract_parameters(build.get("actions"))
        if _params_match(params, expected_params):
            candidates.append({
                "kind": "build",
                "build_url": url,
                "params": params,
            })
    return candidates[0] if candidates else None


def find_duplicate_jenkins_job(cfg, repo_name, job_type="ci", branch=None):
    jk = get_jenkins_cfg(cfg)
    if not jk:
        return None

    base_url = jk["url"].rstrip("/")
    user = jk["user"]
    api_token = jk["api_token"]
    expected_params = _build_jenkins_params(cfg, repo_name, job_type=job_type, branch=branch)
    job_name = get_jenkins_job_name(cfg, repo_name, job_type, env=branch)
    job_path = "/job/".join(job_name.split("/"))
    job_url = "{}/job/{}/".format(base_url, job_path)

    duplicate = _find_duplicate_queue_item(base_url, user, api_token, job_url, expected_params)
    if duplicate:
        duplicate.update({"job_name": job_name, "job_url": job_url})
        return duplicate

    duplicate = _find_duplicate_running_build(base_url, user, api_token, job_path, expected_params)
    if duplicate:
        duplicate.update({"job_name": job_name, "job_url": job_url})
        return duplicate
    return None


def trigger_jenkins_job(cfg, repo_name, job_type="ci", branch=None):
    jk = get_jenkins_cfg(cfg)
    if not jk:
        return False, "Jenkins 未配置", None

    base_url = jk["url"].rstrip("/")
    user = jk["user"]
    api_token = jk["api_token"]
    job_name = get_jenkins_job_name(cfg, repo_name, job_type, env=branch)

    job_path = "/job/".join(job_name.split("/"))
    job_url = "{}/job/{}/".format(base_url, job_path)
    url = "{}/job/{}/buildWithParameters".format(base_url, job_path)
    params = _build_jenkins_params(cfg, repo_name, job_type=job_type, branch=branch)

    try:
        duplicate = find_duplicate_jenkins_job(cfg, repo_name, job_type=job_type, branch=branch)
        if duplicate:
            if duplicate.get("kind") == "queue":
                return True, "检测到相同参数任务已在 Jenkins 队列中，跳过重复触发", {
                    "job_url": duplicate.get("job_url") or job_url,
                    "queue_url": duplicate.get("queue_url"),
                    "build_url": duplicate.get("build_url"),
                    "duplicate_skipped": True,
                    "duplicate_kind": "queue",
                }
            return True, "检测到相同参数任务正在 Jenkins 运行中，跳过重复触发", {
                "job_url": duplicate.get("job_url") or job_url,
                "queue_url": None,
                "build_url": duplicate.get("build_url"),
                "duplicate_skipped": True,
                "duplicate_kind": "build",
            }

        resp = requests.post(url, auth=(user, api_token), params=params, timeout=15, allow_redirects=False)
        if resp.status_code in (200, 201, 202, 302):
            queue_url = resp.headers.get("Location")
            meta = {"job_url": job_url, "queue_url": queue_url}
            if not queue_url:
                duplicate = find_duplicate_jenkins_job(cfg, repo_name, job_type=job_type, branch=branch)
                if duplicate:
                    meta.update({
                        "queue_url": duplicate.get("queue_url"),
                        "build_url": duplicate.get("build_url"),
                        "duplicate_skipped": bool(duplicate.get("kind")),
                        "duplicate_kind": duplicate.get("kind"),
                    })
            return True, "已触发", meta
        elif resp.status_code == 401:
            return False, "Jenkins 认证失败，请检查 user / api_token", {"job_url": job_url}
        elif resp.status_code == 404:
            return False, "Job '{}' 不存在，请检查配置".format(job_name), {"job_url": job_url}
        else:
            return False, "HTTP {}: {}".format(resp.status_code, resp.text[:200]), {"job_url": job_url}
    except requests.exceptions.ConnectionError:
        return False, "无法连接 Jenkins: {}".format(base_url), {"job_url": job_url}
    except Exception as e:
        return False, str(e), {"job_url": job_url}


def _resolve_at_id(member):
    if not member:
        return ""
    return str(member.get("open_id") or member.get("user_id") or member.get("id") or "").strip()


def _resolve_member_name(member):
    if not member:
        return ""
    return str(member.get("name") or member.get("display_name") or member.get("label") or "").strip()


def _normalize_match_text(value):
    return re.sub(r"[^a-z0-9]+", "", str(value or "").strip().lower())


def _match_member_by_name(members, raw_name):
    target = str(raw_name or "").strip()
    if not target:
        return None

    normalized_target = _normalize_match_text(target)
    candidates = []
    for member in members:
        name = _resolve_member_name(member)
        normalized_name = _normalize_match_text(name)
        if not normalized_name:
            continue
        candidates.append((member, name, normalized_name))

    for member, _, normalized_name in candidates:
        if normalized_name == normalized_target:
            return member

    partial_matches = []
    for member, _, normalized_name in candidates:
        if normalized_target and (normalized_target in normalized_name or normalized_name in normalized_target):
            partial_matches.append((member, normalized_name))
    if len(partial_matches) == 1:
        return partial_matches[0][0]
    if len(partial_matches) > 1:
        raise RuntimeError("SQA 成员匹配到多个候选: {}".format(target))

    scored = []
    for member, name, normalized_name in candidates:
        score = difflib.SequenceMatcher(None, normalized_target, normalized_name).ratio()
        scored.append((score, member, name))
    scored.sort(key=lambda item: item[0], reverse=True)
    if scored and scored[0][0] >= 0.6:
        if len(scored) > 1 and abs(scored[0][0] - scored[1][0]) < 0.05:
            raise RuntimeError("SQA 成员匹配不够明确: {}，候选={} / {}".format(target, scored[0][2], scored[1][2]))
        return scored[0][1]
    return None


def _normalize_initiator(initiator_id=None, initiator_name=None, fallback_sender=None):
    normalized_id = str(initiator_id or "").strip()
    normalized_name = str(initiator_name or "").strip()
    if normalized_id or normalized_name:
        return {
            "open_id": normalized_id,
            "user_id": normalized_id,
            "id": normalized_id,
            "name": normalized_name,
        }, False
    return fallback_sender, True


def _at_tag(member):
    if not member:
        return ""
    uid = _resolve_at_id(member)
    name = _resolve_member_name(member)
    return "<at id={}></at>".format(uid) if uid else ("@{}".format(name) if name else "")


def send_feishu_deploy_msg(cfg, env, services, changes, sqa_members, initiator_id=None, initiator_name=None, force=False, job_type="ci"):
    webhook = str(cfg.get("feishu_deploy_webhook") or "").strip()
    notify_envs = cfg.get("deploy_notify_envs", ["test", "demo"])
    sender = cfg.get("deploy_sender")
    if not webhook or "your_webhook_id" in webhook:
        return False, "config.json 中 feishu_deploy_webhook 未配置"
    if (not force) and env not in notify_envs:
        return False, "环境 {} 不在 deploy_notify_envs={} 中".format(env, notify_envs)

    env_display = {"test": "Test", "demo": "Demo", "master": "Production", "prod": "Production"}.get(env, env)
    service_list = "、".join(services)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    initiator, used_fallback_sender = _normalize_initiator(
        initiator_id=initiator_id,
        initiator_name=initiator_name,
        fallback_sender=sender,
    )
    sender_text = _at_tag(initiator)
    if not sender_text and initiator_name:
        sender_text = initiator_name
    if not sender_text and initiator:
        sender_text = _resolve_member_name(initiator)
    if not sender_text and sender and sender is not initiator:
        sender_text = _at_tag(sender) or _resolve_member_name(sender)
        used_fallback_sender = bool(sender_text)
    sqa_text = " ".join([_at_tag(m) for m in sqa_members if _at_tag(m)])

    is_cd = str(job_type or "ci").lower() == "cd"
    header_content = "部署通知" if is_cd else "打包通知"
    header_template = "red" if is_cd else "blue"
    action_text = "构建+部署" if is_cd else "仅打包"

    elements = [
        {
            "tag": "div",
            "fields": [
                {"is_short": True, "text": {"tag": "lark_md", "content": "**涉及服务：**\n{}".format(service_list)}},
                {"is_short": True, "text": {"tag": "lark_md", "content": "**环境：**\n{}".format(env_display)}},
            ],
        },
        {
            "tag": "div",
            "fields": [
                {"is_short": True, "text": {"tag": "lark_md", "content": "**分支：**\n{}".format(env)}},
                {"is_short": True, "text": {"tag": "lark_md", "content": "**类型：**\n{}".format(action_text)}},
            ],
        },
        {"tag": "div", "text": {"tag": "lark_md", "content": "**涉及改动：**{}".format(changes)}},
        {"tag": "hr"},
    ]
    if sender_text or sqa_text:
        sender_content = "**发起人：**{}".format(sender_text) if sender_text else ""
        if used_fallback_sender:
            sender_content += "\n<font color='grey'>（未拿到本次消息发起人 ID，已回退默认发起人）</font>"
        elements.append({
            "tag": "div",
            "fields": [
                {"is_short": True, "text": {"tag": "lark_md", "content": sender_content}},
                {"is_short": True, "text": {"tag": "lark_md", "content": "**SQA：**{}".format(sqa_text) if sqa_text else ""}},
            ],
        })
    elements.append({"tag": "note", "elements": [{"tag": "plain_text", "content": "发送时间: {}".format(now)}]})

    card = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": header_content}, "template": header_template},
            "elements": elements,
        },
    }
    try:
        resp = requests.post(webhook, json=card, timeout=10)
        body = resp.json()
    except Exception as e:
        return False, "发送异常: {}".format(e)
    if resp.status_code == 200 and body.get("StatusCode") == 0:
        return True, "飞书{}已发送".format(header_content)
    return False, "发送失败: HTTP {}, body={}".format(resp.status_code, body)


def resolve_sqa_members(cfg, extra_at_name=None):
    members = list(cfg.get("deploy_at_members", []) or [])
    if not members:
        return []
    if not extra_at_name:
        return [members[0]]
    selected = []
    for raw_name in extra_at_name.split(","):
        target = raw_name.strip()
        if not target:
            continue
        matched = _match_member_by_name(members, target)
        if matched is None:
            raise RuntimeError("未在 config.deploy_at_members 中找到匹配成员: {}".format(target))
        if matched not in selected:
            selected.append(matched)
    return selected


def wait_for_job_completion(cfg, queue_url=None, build_url=None, timeout_seconds=1800, poll_seconds=10):
    if not queue_url and not build_url:
        return False, "未拿到 Jenkins queue/build url，无法等待完成", None
    jk = get_jenkins_cfg(cfg)
    user = jk["user"]
    api_token = jk["api_token"]
    started = time.time()
    build_api = build_url.rstrip("/") + "/api/json" if build_url else None

    while time.time() - started < timeout_seconds:
        if build_api is None:
            qurl = queue_url.rstrip("/") + "/api/json"
            resp = requests.get(qurl, auth=(user, api_token), timeout=15)
            resp.raise_for_status()
            qdata = resp.json()
            executable = qdata.get("executable")
            if executable and executable.get("url"):
                build_api = executable["url"].rstrip("/") + "/api/json"
            else:
                if qdata.get("cancelled"):
                    return False, "Jenkins 队列任务被取消", None
                time.sleep(poll_seconds)
                continue

        resp = requests.get(build_api, auth=(user, api_token), timeout=15)
        resp.raise_for_status()
        bdata = resp.json()
        if bdata.get("building"):
            time.sleep(poll_seconds)
            continue
        result = bdata.get("result")
        final_build_url = bdata.get("url") or build_url
        if result == "SUCCESS":
            return True, "Jenkins 构建成功", final_build_url
        return False, "Jenkins 构建结束但结果为 {}".format(result), final_build_url

    return False, "等待 Jenkins 超时", build_url
