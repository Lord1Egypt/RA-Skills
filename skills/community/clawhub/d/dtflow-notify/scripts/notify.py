#!/usr/bin/env python3
"""
钉钉通知公共模块（统一发送出口）—— 通用脱敏版
================================================
所有定时任务的「私信/工作通知」统一走这里，避免各脚本重复实现。

- 凭证：环境变量 > ~/.dingtalk-skills/config（与既有脚本一致）
- Token：获取失败自动重试；连接/读取超时分离
- 发送：工作通知（text / markdown）、文件
- 失败兜底：发送失败自动写本地日志 logs/dingtalk_fail.log

CLI（供 cron/agent 直接调用）：
  python3 dingtalk_notify.py --text "内容" [--to <userId>]
  python3 dingtalk_notify.py --markdown "内容" [--title "标题"] [--to <userId>]
  python3 dingtalk_notify.py --file /abs/path.pptx [--to <userId>]
  python3 dingtalk_notify.py --dm --markdown "内容" [--title "标题"]        # 机器人私信（特殊）
  python3 notify.py --dm-self --text "内容"                                 # 私信本人（dws 本人身份）
  （不传 --to 时默认发给 DINGTALK_MY_USER_ID）
  通道命名（2026-11-06 定）：
    - 默认(不加参数) = 「工作通知」notify —— 一般通知/结果汇报
    - --dm          = 「机器人私信」—— 特殊情况，少用
    - --dm-self     = 「私信本人」—— dws 以本人身份单聊（优先私信）
    - 群通知走群 Webhook（不在此脚本）

库调用：
  from notify import send_work_notification, send_work_file, upload_file
"""
from __future__ import annotations

import os
import sys
import time
import json
import argparse
from datetime import datetime, timezone, timedelta

import requests

# ------------------------------------------------------------
# 配置
# ------------------------------------------------------------
WORKSPACE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.environ.get("DINGTALK_CONFIG") or os.path.expanduser("~/.dingtalk-skills/config")
FAIL_LOG = os.path.join(os.environ.get("DINGTALK_LOG_DIR")
                        or os.path.expanduser("~/.dingtalk-skills/logs"), "dingtalk_fail.log")

# 钉钉「文件」消息上传上限（Joel 2026-11-12：单文件 ≤ 20MB）
DINGTALK_FILE_LIMIT = 20 * 1024 * 1024

DEFAULT_TIMEOUT = (5, 10)   # (连接超时, 读取超时) —— 统一标准
TOKEN_RETRIES = 1           # token 获取失败后的重试次数
RETRY_SLEEP = 3             # 重试间隔（秒）


def _load_conf():
    conf = {}
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                conf[k.strip()] = v.strip()
    except OSError:
        pass
    return conf


_CONF = _load_conf()


def _cfg(key):
    return os.environ.get(key) or _CONF.get(key, "")


APP_KEY = _cfg("DINGTALK_APP_KEY")
APP_SECRET = _cfg("DINGTALK_APP_SECRET")
AGENT_ID = _cfg("DINGTALK_AGENT_ID")
DEFAULT_USERID = _cfg("DINGTALK_MY_USER_ID")


def _bj_now():
    return datetime.now(timezone(timedelta(hours=8)))


# ------------------------------------------------------------
# 失败兜底日志
# ------------------------------------------------------------
def log_failure(task, detail):
    """记录发送失败到本地日志（静默失败 → 有据可查）"""
    try:
        os.makedirs(os.path.dirname(FAIL_LOG), exist_ok=True)
        with open(FAIL_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{_bj_now().strftime('%Y-%m-%d %H:%M:%S')}] {task} | {detail}\n")
    except OSError:
        pass


# ------------------------------------------------------------
# Token
# ------------------------------------------------------------
def get_token(retries=TOKEN_RETRIES, timeout=DEFAULT_TIMEOUT):
    """获取企业应用 access_token（带重试）。失败返回 None 并记日志。"""
    if not APP_KEY or not APP_SECRET:
        msg = "缺少 DINGTALK_APP_KEY / DINGTALK_APP_SECRET（检查环境变量或 ~/.dingtalk-skills/config）"
        print(f"❌ {msg}")
        log_failure("get_token", msg)
        return None

    last_err = None
    for attempt in range(retries + 1):
        try:
            resp = requests.get(
                "https://oapi.dingtalk.com/gettoken",
                params={"appkey": APP_KEY, "appsecret": APP_SECRET},
                timeout=timeout,
            ).json()
            token = resp.get("access_token")
            if token:
                return token
            last_err = resp.get("errmsg") or resp
        except requests.exceptions.RequestException as e:
            last_err = str(e)
        if attempt < retries:
            print(f"⏳ 取 token 第{attempt+1}次失败，{RETRY_SLEEP}s 后重试...")
            time.sleep(RETRY_SLEEP)

    print(f"❌ 获取 token 失败: {last_err}")
    log_failure("get_token", f"获取失败: {last_err}")
    return None


# ------------------------------------------------------------
# 发送
# ------------------------------------------------------------
def _norm_userid(userid):
    if isinstance(userid, (list, tuple, set)):
        return ",".join(str(x) for x in userid)
    return str(userid)


def send_work_notification(userid=None, content="", msgtype="text", title=None,
                           task="work-notification"):
    """
    发送「工作通知」（私信）。text 或 markdown。
    返回 bool；失败写日志。
    """
    userid = _norm_userid(userid or DEFAULT_USERID)
    token = get_token()
    if not token:
        return False

    if msgtype == "markdown":
        msg = {"msgtype": "markdown",
               "markdown": {"title": title or content[:20], "text": content}}
    else:
        msg = {"msgtype": "text", "text": {"content": content}}

    payload = {"agent_id": AGENT_ID, "userid_list": userid, "msg": msg}
    url = f"https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token={token}"

    try:
        resp = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT).json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 发送异常: {e}")
        log_failure(task, f"发送异常 -> {userid}: {e}")
        return False

    if resp.get("errcode") == 0:
        print(f"✅ 工作通知已发送至 {userid}")
        return True

    print(f"❌ 发送失败: {resp}")
    log_failure(task, f"发送失败 -> {userid}: {resp}")
    return False


def upload_file(file_path, task="media-upload"):
    """上传文件到钉钉媒体服务器，返回 media_id 或 None"""
    token = get_token()
    if not token:
        return None
    filename = os.path.basename(file_path)
    try:
        _sz = os.path.getsize(file_path)
    except OSError:
        _sz = 0
    if _sz > DINGTALK_FILE_LIMIT:
        print(f"❌ 文件 {filename} 为 {_sz/1048576:.1f}MB，超过钉钉上传上限 {DINGTALK_FILE_LIMIT//1048576}MB；请拆分/压缩后再发。")
        log_failure(task, f"文件超限 {_sz} > {DINGTALK_FILE_LIMIT}: {filename}")
        return None
    try:
        with open(file_path, "rb") as f:
            files = {"media": (filename, f,
                     "application/vnd.openxmlformats-officedocument.presentationml.presentation")}
            resp = requests.post(
                f"https://oapi.dingtalk.com/media/upload?access_token={token}",
                data={"type": "file"}, files=files, timeout=(5, 30),
            ).json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 文件上传异常: {e}")
        log_failure(task, f"上传异常 {filename}: {e}")
        return None

    if resp.get("errcode") == 0:
        print(f"✅ 文件已上传: {filename}")
        return resp["media_id"]
    print(f"❌ 文件上传失败: {resp}")
    log_failure(task, f"上传失败 {filename}: {resp}")
    return None


def send_work_file(userid=None, media_id=None, task="work-notification-file"):
    """发送文件工作通知（私信）。返回 bool"""
    userid = _norm_userid(userid or DEFAULT_USERID)
    token = get_token()
    if not token or not media_id:
        return False
    payload = {"agent_id": AGENT_ID, "userid_list": userid,
               "msg": {"msgtype": "file", "file": {"media_id": media_id}}}
    url = f"https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token={token}"
    try:
        resp = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT).json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 文件发送异常: {e}")
        log_failure(task, f"文件发送异常 -> {userid}: {e}")
        return False
    if resp.get("errcode") == 0:
        print(f"✅ 文件工作通知已发送至 {userid}")
        return True
    print(f"❌ 文件工作通知发送失败: {resp}")
    log_failure(task, f"文件发送失败 -> {userid}: {resp}")
    return False


# ------------------------------------------------------------
# 机器人「单聊私信」（真·私信，区别于上面的工作通知）
#   走新版接口 POST https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend
#   需要新版 accessToken（api.dingtalk.com 而非 oapi.dingtalk.com）
# ------------------------------------------------------------
def get_new_token(retries=TOKEN_RETRIES, timeout=DEFAULT_TIMEOUT):
    """获取新版 accessToken（api.dingtalk.com）。失败返回 None 并记日志。"""
    if not APP_KEY or not APP_SECRET:
        print("❌ 缺少 DINGTALK_APP_KEY / DINGTALK_APP_SECRET")
        return None
    last_err = None
    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                "https://api.dingtalk.com/v1.0/oauth2/accessToken",
                json={"appKey": APP_KEY, "appSecret": APP_SECRET},
                timeout=timeout,
            ).json()
            tok = resp.get("accessToken")
            if tok:
                return tok
            last_err = resp.get("message") or resp
        except requests.exceptions.RequestException as e:
            last_err = str(e)
        if attempt < retries:
            time.sleep(RETRY_SLEEP)
    print(f"❌ 获取新版 token 失败: {last_err}")
    log_failure("get_new_token", f"获取失败: {last_err}")
    return None


def send_dm(userid=None, content="", msgtype="markdown", title=None, task="robot-dm"):
    """发送「机器人单聊私信」。msgtype: markdown | text。返回 bool；失败写日志。"""
    userid = _norm_userid(userid or DEFAULT_USERID)
    token = get_new_token()
    if not token:
        return False

    if msgtype == "markdown":
        msg_key = "sampleMarkdown"
        param = {"title": title or (content[:20] if content else ""), "text": content}
    else:
        msg_key = "sampleText"
        param = {"content": content}

    payload = {"robotCode": APP_KEY, "userIds": [u for u in userid.split(",") if u],
               "msgKey": msg_key, "msgParam": json.dumps(param, ensure_ascii=False)}
    url = "https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend"
    try:
        resp = requests.post(
            url,
            headers={"x-acs-dingtalk-access-token": token, "Content-Type": "application/json"},
            data=json.dumps(payload, ensure_ascii=False).encode(),
            timeout=DEFAULT_TIMEOUT,
        ).json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 私信发送异常: {e}")
        log_failure(task, f"私信异常 -> {userid}: {e}")
        return False

    if resp.get("processQueryKey") is not None:
        if resp.get("invalidStaffIdList"):
            print(f"⚠️ 私信已发，但存在无效用户: {resp.get('invalidStaffIdList')}")
        print(f"✅ 私信已发送至 {userid}")
        return True
    print(f"❌ 私信发送失败: {resp}")
    log_failure(task, f"私信失败 -> {userid}: {resp}")
    return False


# ------------------------------------------------------------
# 「私信本人」：用 dws 以本人身份发单聊（dws chat +dm）
# ------------------------------------------------------------
def send_dm_self(content="", to_name=None, task="dm-self"):
    """以本人身份私信（默认发给本人）。返回 bool；失败写日志。"""
    import subprocess
    to_name = to_name or _cfg("DINGTALK_MY_NAME")
    if not to_name:
        print("❌ 未配置 DINGTALK_MY_NAME（--dm-self 需要本人姓名）")
        log_failure(task, "缺少 DINGTALK_MY_NAME")
        return False
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.local/bin") + os.pathsep + env.get("PATH", "")
    try:
        p = subprocess.run(
            ["dws", "chat", "+dm", "--to", to_name, "--content", content,
             "--yes", "--format", "json"],
            capture_output=True, text=True, timeout=120, env=env, cwd=WORKSPACE,
        )
    except Exception as e:
        print(f"❌ 私信本人 执行异常: {e}")
        log_failure(task, f"私信本人异常 -> {to_name}: {e}")
        return False
    out = (p.stdout or "").strip()
    try:
        resp = json.loads(out)
    except Exception:
        resp = {}
    if resp.get("success") is True:
        print(f"✅ 私信本人 已发送（to={to_name}）")
        return True
    print(f"❌ 私信本人 失败: rc={p.returncode} out={out[:300]} err={(p.stderr or '')[:200]}")
    log_failure(task, f"私信本人失败 -> {to_name}: rc={p.returncode} {out[:200]}")
    return False


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------
def _main():
    ap = argparse.ArgumentParser(description="钉钉通知统一发送入口")
    ap.add_argument("--to", default=None, help="接收人 userId（默认 DINGTALK_MY_USER_ID）")
    ap.add_argument("--dm", action="store_true",
                    help="用「机器人单聊私信」发送（默认是「工作通知」）")
    ap.add_argument("--dm-self", action="store_true",
                    help="用「私信本人」(dws chat +dm，以本人身份) 发送")
    ap.add_argument("--name", default=None, help="--dm-self 时的收件人姓名（默认取 DINGTALK_MY_NAME）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text", help="纯文本内容")
    g.add_argument("--markdown", help="Markdown 内容")
    g.add_argument("--file", help="文件绝对路径")
    ap.add_argument("--title", default=None, help="Markdown 标题")
    args = ap.parse_args()

    if args.dm_self:
        if args.file is not None:
            print("❌ 私信本人不支持发送文件，请用工作通知")
            sys.exit(2)
        ok = send_dm_self(args.text if args.text is not None else args.markdown, to_name=args.name)
    elif args.dm:
        if args.file is not None:
            print("❌ 私信(机器人单聊)不支持发送文件，请用工作通知或 --markdown")
            sys.exit(2)
        if args.text is not None:
            ok = send_dm(args.to, args.text, msgtype="text")
        else:
            ok = send_dm(args.to, args.markdown, msgtype="markdown", title=args.title)
    elif args.text is not None:
        ok = send_work_notification(args.to, args.text, msgtype="text")
    elif args.markdown is not None:
        ok = send_work_notification(args.to, args.markdown, msgtype="markdown", title=args.title)
    else:
        mid = upload_file(args.file)
        ok = send_work_file(args.to, mid) if mid else False

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    _main()
