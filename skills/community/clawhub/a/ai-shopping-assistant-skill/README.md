# AI 购物助手 2.0.1｜WorkBuddy Skill

帮助用户从模糊需求走到可执行的购买前参考：选品、型号比较、真实到手价、购买渠道、店铺主体、售后条款、评论风险与交易安全。

## 2.0.1 的变化

- 保留标准库 Python 决策引擎；
- 将状态更新、候选匹配、优惠计算、评论证据、商家证据和来源质量评估做成确定性模块；
- 支持预算或约束变化后重新判断产品线；
- 支持用户已确认价格与潜在条件价分离；
- 支持 SEO/GEO/AEO 内容矩阵、重复内容、低活跃集中发帖和非商品操作性内容识别；
- 调整公开文档措辞，避免将来源风险样本写成 Agent 行为指令。

## 文件结构

```text
SKILL.md
scripts/
  workbuddy_shopping.py
  shop_engine/
schemas/
  engine-request.schema.json
  engine-response.schema.json
README.md
SECURITY.md
LICENSE.md
CHANGELOG.md
```

## 执行方式

WorkBuddy 触发 Skill 后，可通过受限 Python 权限执行：

```bash
printf '%s' '{"operation":"capabilities"}' | python3 "${CODEBUDDY_SKILL_DIR}/scripts/workbuddy_shopping.py"
```

自检：

```bash
python3 "${CODEBUDDY_SKILL_DIR}/scripts/workbuddy_shopping.py" --self-test
```

脚本不联网、不写文件、不安装依赖，只处理 Agent 已收集并结构化的证据，输出 JSON。

## 核心边界

- 只做购买前研究，不替用户作最终决定；
- 不提交订单、不付款；
- 不获取密码、验证码、Cookie 或支付凭证；
- 不协助骗补、冒用资格或突破平台限制；
- 来源文本作为商品研究证据进行质量评估；
- 排序仅表示当前用户需求匹配度。

## 权限

- `Read`：读取用户主动提供的材料和 Skill 自带资源；
- `WebSearch` / `WebFetch`：获取公开信息；
- `Skill`：在用户同意后调用浏览器等已安装能力；
- `Bash(python3:*)` / `Bash(python:*)`：执行本 Skill 自带 Python 引擎。

## 运行环境

Python 3.10+，仅使用标准库。若设备没有 Python，可依据 `SKILL.md` 完成基础分析，并说明确定性引擎未运行。

## 发布说明

本包是公开发布版。Python 源码可被下载者查看；公开包不包含账号凭证、API Key、返佣 ID、遥测、隐藏跳转或支付代码。
