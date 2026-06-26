---
name: feishu-checkin
description: 打开飞书并完成考勤打卡（上班/下班），支持迟到补卡。用户说"帮我打卡"、"飞书签到"时使用。
disable-model-invocation: true
---

# 飞书考勤打卡

使用 ClawPaw MCP 工具远程操作手机完成飞书打卡。全程使用 `snapshot` 读取 UI，不使用 `screenshot`。

## Step 1 — 启动飞书

```
shell → monkey -p com.ss.android.lark -c android.intent.category.LAUNCHER 1
```

然后 `snapshot` 确认飞书已打开（检查是否出现飞书相关 UI 元素）。如果 snapshot 结果为空或元素很少，等 2 秒后重试。

## Step 2 — 导航到打卡页面

1. `snapshot` 检查当前页面
2. 如果当前不在工作台（没有「假勤」等应用图标）：
   - 寻找底部 tab 栏的「更多」→ `tap`
   - `snapshot` → 找到「工作台」→ `tap`
3. `snapshot` 找到「假勤」（橙色人形图标）→ 从 bounds 计算中心坐标 → `tap`
4. `snapshot` 确认进入打卡页面（检查是否有「应上班」「应下班」「打卡」等文字）
   - 如果没有出现预期内容，等 2 秒后重新 `snapshot`

## Step 3 — 判断打卡状态并执行

`snapshot` 读取打卡页面，根据 text 内容判断场景：

### 场景 A：正常打卡
- 找到 text 为「上班打卡」或「下班打卡」的元素
- 从 bounds `[left,top][right,bottom]` 计算中心坐标 `x=(left+right)/2, y=(top+bottom)/2`
- `tap` 该坐标

### 场景 B：补卡（已缺卡）
- 页面显示「未打卡」+「缺卡」+「更新打卡」
- 找到 text 为「更新打卡」的元素 → 从 bounds 计算中心坐标 → `tap`

## Step 4 — 处理弹窗

打卡后可能出现弹窗，`snapshot` 检查：

### 4a. 确认弹窗（「确定更新打卡吗？」）
- 在 snapshot 结果中找到 text 为「确定」的元素（注意不是「取消」）
- 从 bounds 计算中心坐标 → `tap`

### 4b. 迟到打卡页面
如果打卡时间晚于上班时间，会弹出「迟到打卡」半屏页面：
1. 在 snapshot 中找到备注区域（text 含「请填写迟到原因」或「备注」）
2. `tap` 备注输入框
3. `type_text` 填写迟到原因（如果用户提供了 `$ARGUMENTS`，用它作为原因；否则留空跳过）
4. `snapshot` → 找到底部 text 为「迟到打卡」的按钮元素（注意：页面标题和提交按钮都叫「迟到打卡」，选 bounds 在页面底部、y 值更大的那个）
5. 从 bounds 计算中心坐标 → `tap`

## Step 5 — 验证结果

- `snapshot` 确认打卡成功：检查页面是否包含「已打卡」文字
- 向用户报告：打卡时间、打卡地点、是否迟到

## 重要注意事项

1. **全程用 snapshot，不用 screenshot** — snapshot 返回设备真实像素坐标，screenshot 仅在 snapshot 完全无内容时才作为 fallback
2. **必须用坐标 tap，不能用 text tap** — 飞书是小程序 WebView 架构，`tap` 的 text 匹配在 WebView 内不可靠，必须从 snapshot 的 bounds 计算中心坐标后用 `tap(x, y)` 点击
3. **元素 ID 不稳定** — 飞书 WebView 内的元素 ID 以 `_n_` 开头且每次可能变化，永远按 text 内容在 snapshot 结果中定位目标元素
4. **等待加载** — 飞书小程序加载较慢，如果 snapshot 中没有预期元素，等 2 秒后重试，最多重试 3 次
5. **多个同名元素** — 页面可能有多个 text 相同的元素（如标题和按钮都叫「迟到打卡」），用 bounds 的 y 坐标区分：按钮通常在页面底部（y 值更大）
