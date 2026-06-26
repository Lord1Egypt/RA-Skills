# Notification / Message / Modal 命令式反馈

命令式调用的反馈组件，不需要写在 template 中。

## 引入

```typescript
import { Notification, Message, Modal } from '@arco-design/web-vue';
```

## Notification 通知

适合操作结果反馈，停留时间较长。

```typescript
// 成功
Notification.success('操作成功');
Notification.success({ content: '保存成功', closable: true });

// 错误
Notification.error(res.msg || '操作失败');
Notification.error({ content: '请求超时', duration: 5000 });
```

## Message 消息

适合轻量提示，自动消失。

```typescript
Message.success('已复制到剪贴板');
Message.error('复制失败，请手动复制');
Message.error({ content: '错误信息', duration: 5000 });
```

## Modal.confirm 确认对话框

适合危险操作前的二次确认。

```typescript
Modal.confirm({
  title: '确认删除',
  content: `确定要删除"${record.name}"吗？此操作不可恢复！`,
  onOk: () => {
    deleteItem(record.id).then(() => {
      Notification.success('删除成功');
      getList();
    });
  },
});
```

## 错误弹窗（API 请求失败）

```typescript
Modal.confirm({
  title: '请求失败',
  content: res.msg,
  simple: false,
  draggable: true,
  footer: true,
});
```

## 使用场景选择

| 场景 | 组件 |
|---|---|
| 操作成功/失败 | `Notification.success/error` |
| 轻量提示（复制、刷新） | `Message.success/error` |
| 危险操作确认 | `Modal.confirm` |
| API 错误展示 | `Modal.confirm`（带详情） |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 全部三种反馈模式
