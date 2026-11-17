# BidHunter 配置指南（依赖型 Skill 标准件）

本 Skill 核心流程（采集、资质比对、评分、日历、筛选、规则编辑器、诊断、FAQ、示例、统一入口）**零外部依赖**，开箱即用。以下仅配置「可选增强」。

环境检查（只读，不泄露凭据值）：

```bash
python3 scripts/check_environment.py
```

---

## 一、资质规则库（必填，非外部依赖）

编辑 `scripts/qual_rules.json` 填入你的投标主体与能力词：

- 零代码：运行 `python3 bidhunter.py rules edit` → 浏览器图形化编辑，内置「能源/建筑/IT/市政」行业模板一键预填
- 或复制 `scripts/samples/demo_rules.json` 改
- 校验：`python3 qual_check.py --validate-rules qual_rules.json`

不填则 `doctor` 会报 E002（仍为示例占位），基础采集可用但比对全为「需确认」。

---

## 二、MiniMax API（可选 · v2.0+ AI 能力）

依赖 id：`minimax-api`

用途：AI 速读标书、风险条款识别、投标策略建议。仅消耗你的 API 余额，无云端。

官方入口：

- 产品主页：https://www.minimaxi.com/
- 开放平台登录：https://platform.minimaxi.com/login
- 接口密钥页：https://platform.minimaxi.com/user-center/basic-information/interface-key
- 接口文档：https://platform.minimaxi.com/document/guides/chat-model/V2

1. 注册并登录开放平台账号
2. 获取密钥：账户管理 → 接口密钥 → 创建密钥（只申请文本模型调用权限）
3. 写入本地配置文件（权限自动 600，密钥不回显、不上传）：

   ```bash
   mkdir -p ~/.config/bidhunter
   cat > ~/.config/bidhunter/ai.json <<'EOF'
   {"api_key":"你的MiniMaxKey","group_id":"可选","model":"MiniMax-M2.7","base_url":"https://api.minimaxi.com/v1/chat/completions"}
   EOF
   chmod 600 ~/.config/bidhunter/ai.json
   ```

4. 最小验证：

   ```bash
   python3 -c "from scripts.ai.minimax_client import MiniMaxClient; MiniMaxClient.from_config(); print('OK')"
   ```

安全：密钥仅存本地文件；轮换/撤销在 MiniMax 控制台操作；本 Skill 不向任何第三方发送你的数据。

降级：未配置时 AI 功能自动跳过，基础采集研判不受影响。

---

## 三、多通道推送（可选 · v1.2）

用途：把日报推到钉钉 / 企业微信 / 邮件。本项是纯本地配置能力，不绑定任一第三方服务账号，因此未列入依赖清单；缺失时只影响推送，不影响核心流程。

```bash
python3 config_wizard.py        # 交互式，未通过连通性测试不写入
python3 config_wizard.py --show # 脱敏查看当前配置
```

- 钉钉：群设置 → 智能群助手 → 自定义机器人 → 加签（推荐）
- 企业微信：群聊 → 群机器人 → 复制 Webhook
- 邮件：SMTP（如 QQ 邮箱用授权码，非登录密码）

配置文件 `~/.config/bidhunter/push.json` 权限 600，密码/密钥脱敏显示。

降级：未配置时仅生成报告文件，不推送。

---

## 四、标书解析依赖（可选 · v2.0 最佳效果）

依赖 id：`pdf-docx-runtime`

官方包页：https://pypi.org/project/PyPDF2/ 、 https://pypi.org/project/python-docx/

```bash
pip install -r requirements.txt   # PyPDF2 + python-docx
```

降级：未装时 PDF 走正则抽取（部分文本）、DOCX 可能解析不全，仍走 AI 流程但质量下降。

---

## 五、常见问题

- **Q：必须联网吗？** 采集需要访问招投标平台；其余（比对/评分/日历/规则编辑/诊断/FAQ）全本地。
- **Q：会外传我的标讯或资质吗？** 不会。所有比对/评分/画像在本地完成；AI 仅把标书文本发往你自己的 MiniMax Key 对应的 API。
- **Q：配置失败会破坏什么吗？** 不会。检查只读，写入前均连通性测试或原子备份。
