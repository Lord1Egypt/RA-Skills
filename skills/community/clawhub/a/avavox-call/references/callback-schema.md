# 通话记录回调结构

当前开放文档里的“通话记录”不是查询 API，而是回调 payload 说明。

## 1. 回调特性

- 同一通通话可能回调多次
- 应优先用 `sessionId` 做幂等去重
- 回调接收成功后，回调方必须返回：

```json
{
  "success": true
}
```

如果没有收到这段响应，平台会按失败处理并重试。

## 2. 关键字段

基础标识：

- `sessionId`
- `customerId`
- `phoneNumber`
- `taskId`
- `taskName`
- `robotId`
- `robotName`
- `lineId`
- `lineName`

通话状态：

- `callStatus`
- `retryCall`
- `callAttemptNumber`
- `hangupParty`

时长与时间：

- `callDuration`
- `ringDuration`
- `importedAt`
- `callStartTime`
- `callEndTime`

媒体与结构化结果：

- `callRecording`
- `ringbackToneUrl`
- `callTags`
- `resultTags`
- `extractResult`
- `summary`
- `conversationContent`

随路数据：

- `ext`

## 3. 常见状态值

- `unconnected`
- `call_success`
- `line_fault`
- `no_one_answer`
- `timeout`
- `user_refuse`
- `voice_mail`
- `call_remind`
- `unreachable`
- `insufficient_balance`
- `powered_off`
- `service_suspended`
- `invalid_number`
- `call_fail`
- `busy`
- `call_rate_limit`

## 4. 与 skill 的关系

- `customers import` 里传入的 `ext`，会在回调里按对象形式回传
- 如果机器人开启了摘要与分析能力，`summary`、`callTags`、`resultTags`、`extractResult` 才有更高概率返回有效内容
- 当前 skill 不把这个文档包装成“查询通话记录列表”的命令，因为开放文档没有给出对应查询接口
