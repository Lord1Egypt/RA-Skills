## 地图 UI 交互与用户反馈规范

本文件从 `SKILL.md` 中拆分而来，统一约束地图相关操作时的用户反馈方式。

### 1. 必须提供用户反馈的场景

以下场景中，必须通过 Toast / Dialog / 页面状态文本等方式给用户明确反馈，而不仅仅是打日志：

- 地图初始化成功 / 失败
- 地图点击选择坐标点（起点 / 终点）
- POI 检索成功 / 无结果 / 失败
- 路线规划成功 / 失败 / 无结果
- 定位成功 / 失败
- 覆盖物添加 / 删除成功
- 地图视野调整完成
- 用户输入验证失败（如坐标格式错误、必填项为空）
- 网络请求失败 / 超时
- 权限获取失败（包括定位、网络等）

### 2. 反馈方式选择建议

#### 2.1 Toast（推荐用于简单提示）

- 场景：成功提示、简单错误提示、操作确认等。
- 要求：时长建议 2000ms（2 秒），文案简短清晰。

示例：

```ts
import { promptAction } from '@kit.ArkUI';

// 成功提示
promptAction.showToast({
  message: '路线规划成功',
  duration: 2000
});

// 错误提示
promptAction.showToast({
  message: '坐标格式不正确，请检查后重试',
  duration: 2000
});
```

#### 2.2 Dialog（用于重要确认或详细错误）

- 场景：需要用户确认的操作、重要错误信息展示等。

示例：

```ts
import { promptAction } from '@kit.ArkUI';

// 确认对话框
promptAction.showDialog({
  title: '确认删除',
  message: '确定要删除这条路线吗？',
  buttons: [
    { text: '取消', color: '#666666' },
    { text: '确定', color: '#1EB980' }
  ]
}).then((result) => {
  if (result.index === 1) {
    // 用户点击了"确定"
  }
});

// 错误信息对话框
promptAction.showDialog({
  title: '路线规划失败',
  message: '网络连接异常，请检查网络后重试',
  buttons: [{ text: '确定', color: '#1EB980' }]
});
```

#### 2.3 页面状态文本（用于实时状态）

- 场景：需要持续显示的状态信息，如“正在规划路线…”、“路线规划成功！距离：2.5 公里”等。

示例：

```ts
@State statusMessage: string = '请在地图上点击选择起点和终点';

// 在 build() 中
Text(this.statusMessage)
  .fontSize(14)
  .fontColor('#555555');
```

### 3. 错误处理与反馈示例

**推荐模式：同时输出用户友好提示和内部日志。**

```ts
// ✅ 正确：提供用户友好的反馈
try {
  const result = await RunRoutePlanner.planRoute(start, end);
  if (result.success) {
    this.showToast('路线规划成功');
    this.statusMessage = `路线规划成功！距离：${(result.distance / 1000).toFixed(2)} 公里`;
  } else {
    this.showToast(result.error || '路线规划失败，请稍后重试');
    this.statusMessage = result.error || '路线规划失败，请稍后重试';
  }
} catch (err) {
  const userMessage = '网络连接异常，请检查网络后重试';
  this.showToast(userMessage);
  this.statusMessage = userMessage;
  Logger.error('SportHealthMap', { error: err, action: 'planRoute' });
}

// ❌ 错误：仅使用日志，没有用户反馈
try {
  const result = await RunRoutePlanner.planRoute(start, end);
  console.info('Route planning result:', result);
} catch (err) {
  console.error('Route planning failed:', err);
}
```

### 4. 文案规范

- 必须使用简洁、明确的中文消息，避免生硬的技术术语。
- 必须区分「成功 / 失败 / 进行中」三种状态。
- 成功消息：如“路线规划成功”、“起点已选择”。
- 失败消息：说明原因和解决建议，如“坐标格式不正确，请输入形如『纬度,经度』的数值”。
- 进行中消息：明确操作进度，如“正在规划路线，请稍候…”.
- 禁止仅展示 JSON 化的错误对象或英文异常信息给用户。

