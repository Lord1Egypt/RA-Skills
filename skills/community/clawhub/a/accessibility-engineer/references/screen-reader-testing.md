# 读屏器实测（Playbook）

> 适用技能：[skills/a11y-audit](../skills/a11y-audit/SKILL.md)（自动化审计后的实测验收环节）、[skills/keyboard-a11y](../skills/keyboard-a11y/SKILL.md)（焦点与播报类问题的读屏验证）。

> 自动化只能覆盖约 30% 的问题。本篇解决：为什么必须读屏实测、用什么工具、测什么、怎么写一份可复现的测试脚本。

## 何时用本篇

- 自动化审计（axe / 我们的脚本）全绿，但"不确定盲用能不能用"
- 修复动态内容播报、焦点移动、朗读顺序类问题
- 给 QA / 验收写读屏测试用例

## 为什么自动化不够

静态检查能发现缺 alt、缺 label、role 非法；但发现不了：
- 朗读**顺序**错乱（DOM 顺序 ≠ 视觉顺序）
- 动态提示**不播报**（live region 没配）
- 焦点移动后读屏**没跟上**
- `aria-label` 与可见文案**冲突**导致的歧义

这些只能靠真人 + 读屏器。

## 三款主力工具

| 工具 | 平台 | 费用 | 适用 |
|------|------|------|------|
| **NVDA** | Windows | 免费 | 最普及，必测基线 |
| **VoiceOver** | macOS / iOS | 系统自带 | Mac/iOS 生态 |
| **JAWS** | Windows | 商业 | 企业环境常见 |
| Narrator | Windows | 系统自带 | 补充 |

> 至少覆盖 **NVDA + VoiceOver** 两款，能抓到绝大多数真实问题。

## 必测清单

- [ ] 页面加载后读屏先报什么（标题？语言？landmark？）
- [ ] 用 landmark / 标题导航是否顺畅
- [ ] 每个表单控件是否报出**正确标签**与类型/状态（必填、错误）
- [ ] 图片 alt 是否恰当（装饰图被跳过）
- [ ] 链接文本是否独立可懂（不都是"点击这里"）
- [ ] 动态内容（Toast、校验错误、加载完成）是否**自动播报**
- [ ] 键盘操作完，读屏焦点是否与视觉焦点一致
- [ ] 模态打开/关闭，焦点是否进入/归还

## 读屏测试脚本模板（可复制到用例）

```
1. 启动 VoiceOver(NVDA)：mac Cmd+F5 / Win Ctrl+NVDA+N
2. 打开目标页面，听首屏播报，记录是否正常
3. 用标题导航（VO+U→标题 / NVDA H）走一遍结构
4. Tab 走一遍所有可聚焦元素，记录每个的名称/角色/状态
5. 触发一个动态操作（提交空表单 / 打开弹窗），验证是否播报
6. 关闭弹窗，验证焦点回到触发处
7. 记录失败点：现象 → 期望 → 对应 SC
```

## 快捷键速查

**VoiceOver (mac)**：`VO(Ctrl+Opt)+→/←` 移动；`VO+U` 转子（标题/链接/landmark）；`VO+A` 从头读。
**NVDA (win)**：`NVDA+↓` 连续朗读；`H` 跳标题；`F` 跳表单；`B` 跳按钮；`D` 跳 landmark；`R` 跳 landmark 间。

## 只在读屏下暴露的典型缺陷

| 现象 | 根因 | 修法 |
|------|------|------|
| 更新不播报 | 缺 `aria-live` / `role="alert"` | 加 live region |
| 焦点移了但没朗读 | 移动的是容器而非可聚焦元素 | `.focus()` 到可聚焦节点 |
| 朗读名与所见不符 | `aria-label` 覆盖 | 让可见文本即名称 |
| 跳过了重要内容 | 误用 `aria-hidden` | 检查是否含可聚焦后代 |

## 相关衔接

- 键盘与焦点是读屏实测的必验项 → `keyboard-focus.md`（焦点陷阱、skip link、roving tabindex）
- 读屏消费的是语义与 ARIA → `semantic-html-aria.md`
- 实测发现的缺陷汇入整改流程 → `audit-remediation.md`
- 读屏实测是整页静态审计的人工补充面 → [skills/a11y-audit](../skills/a11y-audit/SKILL.md)
- 静态面由脚本负责：[scripts/a11y_audit.py](../scripts/a11y_audit.py)、[scripts/aria_lint.py](../scripts/aria_lint.py)

## 限制

- 读屏测试依赖具体软件版本，结果以"能/不能用"定性，难以写死断言；它补自动化之不足，不取代 `a11y_audit.py` / `aria_lint.py`。
- 真机/真软件测试不在本仓库脚本能力内；脚本负责静态面，本篇负责人工面。
