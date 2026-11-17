# 9项就绪检查详细方法论

> 每项检查包含：检查目的 / 检查方法 / 通过标准 / 常见失败原因 / 修复建议

---

## 检查1: 脚本可独立运行

**目的：** 确保生成的执行器脚本不依赖会话上下文，可被 TRAE agent 独立调用。

**检查方法：**
```bash
cd "<project_root>" && python "<script_path>" --dry-run
```
（如果有 --dry-run 参数；否则直接运行并观察是否报错）

**通过标准：**
- 脚本启动无 ImportError / ModuleNotFoundError
- 脚本启动无 NameError（引用了会话中定义但未写入脚本的变量）
- 脚本退出码为 0（或预期内的非零码）

**常见失败原因：**
| 原因 | 修复建议 |
|------|---------|
| 脚本引用了会话中定义的变量 | 将变量提取为命令行参数或环境变量 |
| 缺少依赖包 | 在脚本头部添加 pip install 检查，或生成 requirements.txt |
| 相对路径错误 | 脚本顶部添加 `os.chdir(os.path.dirname(__file__))` 或使用绝对路径 |
| 硬编码了调试时的临时路径 | 替换为可配置路径或环境变量 |

---

## 检查2: 环境变量齐全

**目的：** 确保所有依赖的环境变量已在系统中配置。

**检查方法：**
```python
import os
required_vars = ["FEISHU_APP_ID", "FEISHU_APP_SECRET", "FEISHU_USER_OPEN_ID"]
for var in required_vars:
    val = os.environ.get(var)
    if not val:
        print(f"❌ 缺失: {var}")
    elif val.startswith("your_") or val == "dummy":
        print(f"⚠️ 占位符: {var}")
    else:
        print(f"✅ {var}: {val[:8]}...")
```

**通过标准：** 所有必需环境变量已配置，且非占位符值。

**常见环境变量清单：**
| 变量名 | 用途 | scope |
|--------|------|-------|
| FEISHU_APP_ID | 飞书应用ID | User |
| FEISHU_APP_SECRET | 飞书应用密钥 | User |
| FEISHU_USER_OPEN_ID | 飞书用户OpenID | User |
| IMA_OPENAPI_CLIENTID | IMA API客户端ID | User |
| IMA_OPENAPI_APIKEY | IMA API密钥 | User |
| GH_TOKEN | GitHub Token | User |
| CLAWHUB_TOKEN | ClawHub Token | User |

---

## 检查3: 数据源可达

**目的：** 确保脚本依赖的外部数据源（API/文件/数据库）可正常访问。

**检查方法：**
- **API：** `curl -s -o /dev/null -w "%{http_code}" <url>` 返回 200
- **文件：** `Test-Path <file_path>` 返回 True
- **数据库：** 尝试连接并执行简单查询

**通过标准：** 所有数据源返回预期响应。

---

## 检查4: IM凭证有效

**目的：** 确保飞书API凭证有效，可发送卡片消息。

**检查方法：**
```python
import requests, os
app_id = os.environ["FEISHU_APP_ID"]
app_secret = os.environ["FEISHU_APP_SECRET"]
resp = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal", 
    json={"app_id": app_id, "app_secret": app_secret})
if resp.status_code == 200 and "tenant_access_token" in resp.json():
    print("✅ 飞书凭证有效")
else:
    print(f"❌ 飞书凭证无效: {resp.json()}")
```

**通过标准：** 成功获取 tenant_access_token。

---

## 检查5: 归档路径存在

**目的：** 确保三端归档目标路径均已确认且可达。

**检查方法：**

**飞书云盘：**
- 确认 folder_token（用 lark-drive skill 的 drive +list 查看文件夹）
- 或确认文件夹路径，由脚本自动创建

**Obsidian inbox：**
- 确认本地目录存在：`Test-Path "<obsidian_inbox_path>"`
- 不存在则创建：`New-Item -ItemType Directory -Force`

**IMA知识库：**
- 确认 kb_id（用 IMA API search_knowledge_base 搜索知识库名）
- 已知 FIM知识库 ID: 从环境变量 `IMA_KB_ID` 读取，或用 search_knowledge_base 搜索获取

**通过标准：** 三端路径均已确认可达。

---

## 检查6: 幂等性

**目的：** 确保重复运行不会产生重复数据。

**检查方法：** 审查脚本逻辑，确认包含以下机制之一：
- **按日期去重：** 文件名含日期 `report-2026-07-11.md`，同日重跑覆盖
- **按ID去重：** 数据库记录有唯一约束
- **跳过逻辑：** 检查输出是否已存在，存在则跳过
- **覆盖逻辑：** 明确的 overwrite=True 参数

**通过标准：** 脚本中有明确的幂等性机制。

**常见失败原因：**
| 原因 | 修复建议 |
|------|---------|
| 文件名无日期 | 添加 `{date}` 占位符 |
| 数据库无唯一约束 | 添加 UPSERT 逻辑 |
| 无存在性检查 | 添加 `if os.path.exists(): skip` |

---

## 检查7: 失败回退链路

**目的：** 确保主脚本失败时有明确的降级方案。

**检查方法：** 确认 Schedule message 中包含分步回退方案：
```
如果主执行器失败，回退到分步：
1. python scripts/step1_fetch.py
2. python scripts/step2_process.py
3. python scripts/step3_output.py
```

**通过标准：** 有至少2层的回退方案（主脚本 → 分步执行 → 手动提示）。

---

## 检查8: 调度频率合理

**目的：** 确保cron频率与任务实际需求匹配。

**合理性参考表：**
| 任务类型 | 建议频率 | cron示例 |
|---------|---------|---------|
| 数据抓取/日报 | 每日1次 | `0 9 * * *` |
| 监控告警 | 每小时 | `0 * * * *` |
| 周报汇总 | 每周1次 | `0 9 * * 1` |
| 月度统计 | 每月1次 | `0 9 1 * *` |
| 实时性要求高 | 每10分钟 | `*/10 * * * *` |

**TRAE Schedule 限制：**
- 最小间隔：10分钟
- 不支持秒级
- 5字段格式：分 时 日 月 周

**通过标准：** 频率与任务需求匹配，不低于10分钟间隔。

---

## 检查9: 输出质量自检

**目的：** 确保简报内容有实质信息，非空壳或模板填充。

**检查方法：** 运行脚本后检查输出：
- **非空检查：** 输出文件大小 > 1KB
- **内容检查：** 不包含 "TODO"、"placeholder"、"lorem ipsum"
- **结构检查：** 包含预期章节（标题/摘要/详情/数据）
- **字数检查：** 简报类输出 800-1000 字，数据类输出有实际数据行

**通过标准：** 输出内容有实质信息，满足以上4项检查。

---

## 检查结果汇总模板

```
## 就绪检查报告

| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 脚本可独立运行 | ✅/❌/⚠️ | <详情> |
| 2 | 环境变量齐全 | ✅/❌/⚠️ | <详情> |
| 3 | 数据源可达 | ✅/❌/⚠️ | <详情> |
| 4 | IM凭证有效 | ✅/❌/⚠️ | <详情> |
| 5 | 归档路径存在 | ✅/❌/⚠️ | <详情> |
| 6 | 幂等性 | ✅/❌/⚠️ | <详情> |
| 7 | 失败回退链路 | ✅/❌/⚠️ | <详情> |
| 8 | 调度频率合理 | ✅/❌/⚠️ | <详情> |
| 9 | 输出质量自检 | ✅/❌/⚠️ | <详情> |

### 汇总
- 通过: <N>/9
- 需修复: <列表>
- 可跳过(用户确认): <列表>
```
