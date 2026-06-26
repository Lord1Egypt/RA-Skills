import json
import os
import requests

# ===================== 配置（优先从环境变量读取） =====================
# 支持的环境变量：
#   YUNXIAO_PERSONAL_TOKEN   — 云效个人访问令牌
#   YUNXIAO_ORGANIZATION_ID  — 企业/组织 ID
#   WECOM_WEBHOOK_URL        — 各种平台的机器人 Webhook 地址
#
# 未设置环境变量时使用下方默认值（可留空，留空则对应功能不可用）

CONFIG = {
    "DOMAIN": "openapi-rdc.aliyuncs.com",
    "PERSONAL_TOKEN": os.environ.get("YUNXIAO_PERSONAL_TOKEN" ),  # 个人令牌
    "ORGANIZATION_ID": os.environ.get("YUNXIAO_ORGANIZATION_ID"),  # 企业/组织ID
    "DEFAULT_REPO_ID": "5230762",          # 代码库ID
    "DEFAULT_SOURCE": "260309_espu_inventory",  # 默认源分支
    "DEFAULT_TARGET": "beta",              # 默认目标分支
    "DEFAULT_FLOW_ID": "4297451",          # 发布流水线ID
    "WECOM_WEBHOOK": os.environ.get("WECOM_WEBHOOK_URL",),  # 机器人地址
    "CHECK_MR_INTERVAL": 30                # MR合并状态检查间隔（秒）
}
# ================================================================

HEADERS = {
    "Content-Type": "application/json",
    "x-yunxiao-token": f"{CONFIG['PERSONAL_TOKEN']}"
}

# MR 状态中文映射
MR_STATUS_MAP = {
    "OPEN": "待合并",
    "MERGED": "已合并",
    "CLOSED": "已关闭",
    "REJECTED": "已拒绝",
    "UNDER_REVIEW": "审核中",
}


# ===================== 大模型意图解析 =====================
async def parse_intent_by_llm(ctx, query: str) -> dict:
    """
    使用大模型解析用户输入，提取操作意图、代码库名称、源分支、目标分支、流水线ID、MR编号、环境关键字。
    返回结构：
    {
        "action": "create_mr" | "query_mr" | "deploy" | "unknown",
        "repo_name": "仓库名或null",
        "source_branch": "源分支名或null",
        "target_branch": "目标分支名或null",
        "flow_id": "流水线ID或null",
        "mr_id": "MR编号（数字字符串）或null",
        "env_keyword": "环境关键字如 beta/dev/master 或null"
    }
    """
    prompt = f"""你是一个代码管理助手，请从用户的指令中提取以下信息，以JSON格式返回，不要输出任何其他内容：

{{
  "action": "create_mr 或 query_mr 或 deploy 或 unknown",
  "repo_name": "代码库名称（字符串，找不到则为 null）",
  "source_branch": "源分支名（字符串，找不到则为 null）",
  "target_branch": "目标分支名（字符串，找不到则为 null）",
  "flow_id": "流水线ID（纯数字字符串，找不到则为 null）",
  "mr_id": "MR编号（纯数字字符串，找不到则为 null）",
  "env_keyword": "环境关键字如 beta、dev、test、master、prod（字符串，找不到则为 null）"
}}

规则：
- 如果用户想创建合并请求 / MR / PR / merge request，action = "create_mr"
- 如果用户想查询MR状态 / 查看合并情况 / MR有没有合并 / 查一下MR，action = "query_mr"
- 如果用户想发布 / 上线 / 部署 / 触发流水线 / 发布到某个环境，action = "deploy"
- 分支名通常是 dev、test、beta、main、master、release、feature/xxx、fix/xxx 或其他用户明确提到的名字
- 代码库名通常是英文项目名、服务名、仓库名
- 流水线ID通常是纯数字
- MR编号通常是 # 后面的数字，或者用户说"第XXX号MR"
- env_keyword 从用户提到的环境名提取，如 beta、dev、test、master，用于搜索流水线。若用户明确指定了 flow_id，env_keyword 可为 null
- 发布场景：若用户说"发布 erp-ops 的 beta 环境"，repo_name="erp-ops", env_keyword="beta", action="deploy"

用户指令：{query}

请直接输出JSON，不要有任何说明文字："""

    try:
        response = await ctx.llm(prompt)
        # 清理可能的 markdown 代码块
        text = response.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        result = json.loads(text)
        return result
    except Exception as e:
        # LLM解析失败时返回 unknown
        return {
            "action": "unknown",
            "repo_name": None,
            "source_branch": None,
            "target_branch": None,
            "flow_id": None,
            "mr_id": None,
            "env_keyword": None,
            "_parse_error": str(e)
        }


# ===================== 发送通知 =====================
def send_wecom(content):
    data = {
        "msgtype": "text",
        "text": {"content": f"【云效通知】\n{content}"}
    }
    try:
        requests.post(CONFIG["WECOM_WEBHOOK"], json=data, timeout=5)
    except:
        pass


# ===================== 按名称查询仓库ID =====================
def get_repo_id_by_name(repo_name: str, exact_match: bool = True) -> dict:
    """
    根据仓库名称查询仓库ID，返回 {仓库名: 仓库ID} 字典。
    exact_match=True 精确匹配，False 模糊匹配。
    """
    url = (
        f"https://{CONFIG['DOMAIN']}/openapi/v1/codeup/organizations/{CONFIG['ORGANIZATION_ID']}/repositories"
    )
    request_body = {
        "search": repo_name,
        "perPage": 100,
        "page": 1,
    }
    try:
        resp = requests.get(url=url, headers=HEADERS, json=request_body, timeout=15)
        if resp.status_code != 200:
            send_wecom(f"❌ 查询仓库列表失败：{resp.status_code} - {resp.text}")
            return {}

        repo_list = resp.json()
        match_repos = {}
        for repo in repo_list:
            repo_id = repo.get("id")
            repo_name_api = repo.get("name", "").strip()
            if not repo_id or not repo_name_api:
                continue
            if exact_match and repo_name_api == repo_name:
                match_repos[repo_name_api] = repo_id
                break
            elif not exact_match and repo_name.lower() in repo_name_api.lower():
                match_repos[repo_name_api] = repo_id

        return match_repos
    except Exception as e:
        print(f"❌ 查询仓库ID异常：{str(e)}")
        return {}


# ===================== 创建 MR =====================
def create_mr(repo_id, source, target):
    url = (
        f"https://{CONFIG['DOMAIN']}/oapi/v1/codeup/organizations/{CONFIG['ORGANIZATION_ID']}"
        f"/repositories/{repo_id}/changeRequests"
    )
    data = {
        "createFrom": "WEB",
        "description": "WorkBuddy 创建",
        "reviewerUserIds": [],
        "sourceBranch": source,
        "sourceProjectId": repo_id,
        "targetBranch": target,
        "targetProjectId": repo_id,
        "title": f"[{source} → {target}] 自动合并请求",
        "triggerAIReviewRun": False,
        "workItemIds": []
    }
    resp = requests.post(url, json=data, headers=HEADERS, timeout=15)
    return resp.json(), resp.status_code, url


# ===================== 查询单个 MR 状态 =====================
def get_mr_status(repo_id, mr_id):
    url = (
        f"https://{CONFIG['DOMAIN']}/oapi/v1/codeup/organizations/{CONFIG['ORGANIZATION_ID']}"
        f"/repositories/{repo_id}/changeRequests/{mr_id}"
    )
    resp = requests.get(url, headers=HEADERS, timeout=10)
    return resp.json() if resp.status_code == 200 else None


# ===================== 按关键字搜索流水线 =====================
def search_pipelines(repo_name: str = None, env_keyword: str = None) -> list:
    """
    搜索流水线，支持按代码库名 + 环境关键字过滤。
    流水线命名规律：{repo_name}_{env_keyword}，如 erp-ops_beta、erp-ops-api_dev
    API 支持 pipelineName 参数做服务端模糊搜索，优先用 repo_name 作为搜索词减少传输量。
    返回列表：[{"pipelineId": xxx, "pipelineName": "xxx"}, ...]
    """
    url = f"https://{CONFIG['DOMAIN']}/oapi/v1/flow/organizations/{CONFIG['ORGANIZATION_ID']}/pipelines"
    results = []
    page = 1
    per_page = 100
    # 用 repo_name 作为服务端搜索词（API支持 pipelineName 参数模糊匹配）
    search_name = repo_name or env_keyword or ""

    while True:
        params = {"perPage": per_page, "page": page}
        if search_name:
            params["pipelineName"] = search_name
        try:
            resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
            if resp.status_code != 200:
                break
            batch = resp.json()
            if not batch:
                break
            results.extend(batch)
            if len(batch) < per_page:
                break
            page += 1
        except Exception as e:
            print(f"❌ 搜索流水线异常：{str(e)}")
            break

    # 客户端再按 repo_name 和 env_keyword 精确过滤（避免服务端模糊搜索引入噪音）
    filtered = []
    for p in results:
        name = p.get("pipelineName", "").lower()
        match_repo = (not repo_name) or (repo_name.lower() in name)
        match_env = (not env_keyword) or (env_keyword.lower() in name)
        if match_repo and match_env:
            filtered.append(p)

    return filtered


# ===================== 触发发布流水线 =====================
def run_publish(flow_id):
    url = f"https://{CONFIG['DOMAIN']}/oapi/v1/flow/pipelines/{flow_id}/runs"
    resp = requests.post(url, headers=HEADERS, timeout=15)
    return resp.json(), resp.status_code


# ===================== WorkBuddy 入口（大模型解析版）=====================
async def skill_handler(ctx, query: str):
    # -------- 第一步：用大模型解析意图 --------
    intent = await parse_intent_by_llm(ctx, query)
    action = intent.get("action", "unknown")

    # -------- 第二步：根据意图执行操作 --------

    # ===== 创建 MR =====
    if action == "create_mr":
        repo_name = intent.get("repo_name")
        src = intent.get("source_branch") or CONFIG["DEFAULT_SOURCE"]
        dst = intent.get("target_branch") or CONFIG["DEFAULT_TARGET"]

        # 解析代码库ID
        if repo_name:
            repo_map = get_repo_id_by_name(repo_name, exact_match=True)
            if not repo_map:
                repo_map = get_repo_id_by_name(repo_name, exact_match=False)

            if not repo_map:
                msg = f"❌ 未找到代码库「{repo_name}」，请确认名称后重试"
                send_wecom(msg)
                return msg

            if len(repo_map) > 1:
                names = "\n".join([f"  · {n}（ID: {rid}）" for n, rid in repo_map.items()])
                msg = f"⚠️ 找到多个匹配的代码库，请补充完整名称：\n{names}"
                return msg

            repo_display, repo_id = next(iter(repo_map.items()))
        else:
            repo_id = CONFIG["DEFAULT_REPO_ID"]
            repo_display = f"默认仓库（ID: {repo_id}）"

        data, code, url = create_mr(repo_id, src, dst)
        if 200 <= code < 300:
            mr_id = data.get("localId")
            mr_url = data.get("detailUrl")
            msg = (
                f"✅ MR创建成功\n"
                f"代码库：{repo_display}\n"
                f"{src} → {dst}\n"
                f"MR ID：#{mr_id}\n"
                f"链接：{mr_url}"
            )
            send_wecom(msg)
            return msg
        else:
            err = f"❌ MR创建失败（HTTP {code}）：{json.dumps(data, ensure_ascii=False)}"
            send_wecom(err)
            return err

    # ===== 查询 MR 状态 =====
    if action == "query_mr":
        repo_name = intent.get("repo_name")
        mr_id = intent.get("mr_id")

        if not mr_id:
            return "❌ 请提供 MR 编号，例如：「查询 erp-ops #425 的合并状态」"

        # 解析代码库ID
        if repo_name:
            repo_map = get_repo_id_by_name(repo_name, exact_match=True)
            if not repo_map:
                repo_map = get_repo_id_by_name(repo_name, exact_match=False)
            if not repo_map:
                return f"❌ 未找到代码库「{repo_name}」"
            if len(repo_map) > 1:
                names = "\n".join([f"  · {n}（ID: {rid}）" for n, rid in repo_map.items()])
                return f"⚠️ 找到多个匹配的代码库，请补充完整名称：\n{names}"
            repo_display, repo_id = next(iter(repo_map.items()))
        else:
            repo_id = CONFIG["DEFAULT_REPO_ID"]
            repo_display = f"默认仓库（ID: {repo_id}）"

        detail = get_mr_status(repo_id, mr_id)
        if not detail:
            return f"❌ 查询 MR #{mr_id} 失败，请确认代码库和MR编号是否正确"

        status_raw = detail.get("status", "UNKNOWN")
        status_cn = MR_STATUS_MAP.get(status_raw, status_raw)
        src = detail.get("sourceBranch", "?")
        dst = detail.get("targetBranch", "?")
        author = detail.get("author", {}).get("name", "?")
        mr_url = detail.get("detailUrl", "")
        title = detail.get("title", "")
        update_time = detail.get("updateTime", "")[:19].replace("T", " ") if detail.get("updateTime") else ""

        # 审核人汇总
        reviewers = detail.get("reviewers", [])
        reviewer_lines = []
        for rv in reviewers:
            rv_name = rv.get("name", "?")
            rv_status = "✅ 已通过" if rv.get("reviewOpinionStatus") == "PASS" else "⏳ 待审核"
            reviewer_lines.append(f"  · {rv_name}：{rv_status}")
        reviewer_str = "\n".join(reviewer_lines) if reviewer_lines else "  · 暂无审核人"

        msg = (
            f"📋 MR 状态查询\n"
            f"代码库：{repo_display}\n"
            f"MR #{mr_id}：{title}\n"
            f"分支：{src} → {dst}\n"
            f"状态：{status_cn}\n"
            f"创建人：{author}\n"
            f"更新时间：{update_time}\n"
            f"审核情况：\n{reviewer_str}\n"
            f"链接：{mr_url}"
        )
        return msg

    # ===== 发布（支持按代码库+环境关键字搜索流水线）=====
    if action == "deploy":
        flow_id = intent.get("flow_id")
        repo_name = intent.get("repo_name")
        env_keyword = intent.get("env_keyword")

        # 若直接提供了 flow_id，跳过搜索
        if not flow_id:
            if not repo_name and not env_keyword:
                flow_id = CONFIG["DEFAULT_FLOW_ID"]
                pipeline_display = f"默认流水线（ID: {flow_id}）"
            else:
                # 按关键字搜索流水线
                matched = search_pipelines(repo_name=repo_name, env_keyword=env_keyword)

                if not matched:
                    hint = []
                    if repo_name:
                        hint.append(f"代码库「{repo_name}」")
                    if env_keyword:
                        hint.append(f"环境「{env_keyword}」")
                    return f"❌ 未找到匹配的流水线（{' + '.join(hint)}），请确认关键字后重试"

                if len(matched) > 1:
                    lines = "\n".join([f"  · {p['pipelineName']}（ID: {p['pipelineId']}）" for p in matched])
                    return (
                        f"⚠️ 找到 {len(matched)} 条匹配的流水线，请指定流水线ID：\n{lines}"
                    )

                flow_id = str(matched[0]["pipelineId"])
                pipeline_display = f"{matched[0]['pipelineName']}（ID: {flow_id}）"
        else:
            pipeline_display = f"流水线 ID: {flow_id}"

        data, code = run_publish(flow_id)
        if 200 <= code < 300:
            msg = f"🚀 发布已触发\n{pipeline_display}"
            send_wecom(msg)
            return msg + "\n✅ 已发通知"
        else:
            err = f"❌ 发布失败（HTTP {code}）：{json.dumps(data, ensure_ascii=False)}"
            send_wecom(err)
            return err

    # ===== 未识别意图 =====
    return (
        "抱歉，我没有理解你的指令。支持的操作：\n\n"
        "**创建 MR**\n"
        "• 帮我把 feature/login 合到 dev\n"
        "• 在 erp-ops 仓库从 fix_xxx 创建到 beta 的 MR\n\n"
        "**查询 MR 状态**\n"
        "• 查询 erp-ops #425 的合并状态\n"
        "• erp-ops-api 第152号MR合并了吗\n\n"
        "**触发发布**\n"
        "• 发布 erp-ops 的 beta 环境\n"
        "• 触发 erp-ops-api dev 流水线\n"
        "• 触发流水线 4297451"
    )
