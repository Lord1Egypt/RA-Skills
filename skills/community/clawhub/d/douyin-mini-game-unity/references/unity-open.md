# 开放能力-扩展

> 基于官方文档: 开放能力 API - 侧边栏、收藏、群聊、直播、互推、排行榜、公会群、数据分析
> 生成时间: 2026-06-24

> ⚠️ **【安全声明】**：
> - **用户标识**：`OpenId`、`AwemeId` 等永久用户标识严禁打印到生产日志，已用 `#if UNITY_EDITOR || DEVELOPMENT_BUILD` 条件编译包裹
> - **数据分析**：`ReportAnalytics`/`ReportScene` 上报数据会关联用户身份，应在用户同意隐私政策后启用，`eventData` 中不得包含敏感凭证
> - **邀请数据**：邀请相关的 `openId`/`inviterId` 等用户 ID 不应记录到生产日志
> - 所有含敏感数据的 `Debug.Log` 均已添加条件编译守卫，复制示例时请保持守卫不变

## 一、侧边栏与场景

### 1.1 TT.CheckScene

**说明**: 检查当前场景是否可用，通常用于判断是否处于抖音宿主环境中的某个特定场景（如侧边栏、游戏中心等）。

**语法**:

```csharp
public static void CheckScene(string scene, Action<bool> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| scene | string | 是 | - | 场景标识，如 "sidebar"、"gameCenter" 等 |
| callback | Action\<bool\> | 是 | - | 回调，参数为 true 表示该场景可用 |

**代码示例**:

```csharp
TT.CheckScene("sidebar", (available) =>
{
    if (available)
    {
        Debug.Log("当前处于侧边栏场景，可使用侧边栏相关能力");
    }
    else
    {
        Debug.Log("当前不在侧边栏场景");
    }
});
```

---

### 1.2 TT.NavigateToScene

**说明**: 导航到指定场景，如从游戏内跳转到侧边栏、游戏中心等。

**语法**:

```csharp
public static void NavigateToScene(string scene, Action success = null, Action<ErrorInfo> fail = null, Action complete = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| scene | string | 是 | - | 目标场景标识 |
| success | Action | 否 | null | 导航成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 导航失败回调 |
| complete | Action | 否 | null | 导航完成回调（成功/失败均触发） |

**代码示例**:

```csharp
TT.NavigateToScene("sidebar",
    success: () => Debug.Log("已导航到侧边栏"),
    fail: (error) => Debug.Log($"导航失败: {error.ErrMsg} ({error.ErrorCode})"),
    complete: () => Debug.Log("导航流程结束")
);
```

---

### 1.3 TT.RequestPromotionActivity

**说明**: 请求获取推广活动信息，用于在侧边栏等场景中展示活动入口。

**语法**:

```csharp
public static void RequestPromotionActivity(Action<PromotionActivityResult> success, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| success | Action\<PromotionActivityResult\> | 是 | - | 成功回调，返回活动数据 |
| fail | Action\<ErrorInfo\> | 否 | null | 失败回调 |

**代码示例**:

```csharp
TT.RequestPromotionActivity(
    success: (result) =>
    {
        Debug.Log($"活动ID: {result.ActivityId}");
        Debug.Log($"活动状态: {result.Status}");
    },
    fail: (error) => Debug.Log($"获取活动失败: {error.ErrMsg}")
);
```

---

### 1.4 TT.ReceiveCoupon

**说明**: 用户领取优惠券，通常与推广活动配合使用。

**语法**:

```csharp
public static void ReceiveCoupon(string activityId, Action success = null, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| activityId | string | 是 | - | 活动 ID |
| success | Action | 否 | null | 领取成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 领取失败回调 |

**代码示例**:

```csharp
TT.ReceiveCoupon("activity_12345",
    success: () => Debug.Log("优惠券领取成功"),
    fail: (error) => Debug.Log($"领取失败: {error.ErrMsg} ({error.ErrorCode})")
);
```

---

## 二、收藏

### 2.1 TT.ShowFavoriteGuide

**说明**: 显示收藏引导弹窗，提示用户将游戏添加到抖音收藏列表。

**语法**:

```csharp
public static void ShowFavoriteGuide(Action<bool> callback = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| callback | Action\<bool\> | 否 | null | 回调，参数表示用户是否完成收藏操作 |

**代码示例**:

```csharp
TT.ShowFavoriteGuide((success) =>
{
    if (success)
    {
        Debug.Log("用户已收藏游戏");
        // 可以给予收藏奖励
    }
    else
    {
        Debug.Log("用户取消收藏");
    }
});
```

---

## 三、群聊

### 3.1 TT.JoinGroup

**说明**: 引导用户加入指定的抖音群。

**语法**:

```csharp
public static void JoinGroup(string groupId, Action success = null, Action<ErrorInfo> fail = null, Action complete = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| groupId | string | 是 | - | 目标群 ID |
| success | Action | 否 | null | 加入成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 加入失败回调 |
| complete | Action | 否 | null | 操作完成回调 |

**代码示例**:

```csharp
TT.JoinGroup("group_xxxxx",
    success: () => Debug.Log("已加入群聊"),
    fail: (error) => Debug.Log($"加入失败: {error.ErrMsg}"),
    complete: () => Debug.Log("入群流程结束")
);
```

---

### 3.2 TT.CheckGroupInfo

**说明**: 查询指定群聊的基本信息。

**语法**:

```csharp
public static void CheckGroupInfo(string groupId, Action<GroupInfoResult> success, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| groupId | string | 是 | - | 群 ID |
| success | Action\<GroupInfoResult\> | 是 | - | 成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 失败回调 |

**代码示例**:

```csharp
TT.CheckGroupInfo("group_xxxxx",
    success: (result) =>
    {
        Debug.Log($"群名称: {result.GroupName}");
        Debug.Log($"成员数: {result.MemberCount}");
        Debug.Log($"当前用户是否在群中: {result.IsInGroup}");
    },
    fail: (error) => Debug.Log($"查询失败: {error.ErrMsg}")
);
```

---

## 四、关注抖音号

### 4.1 TT.CheckFollowAwemeState

**说明**: 检查用户是否已关注指定的抖音号。

**语法**:

```csharp
public static void CheckFollowAwemeState(Action<FollowStateResult> success, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| success | Action\<FollowStateResult\> | 是 | - | 成功回调，返回关注状态 |
| fail | Action\<ErrorInfo\> | 否 | null | 失败回调 |

**代码示例**:

```csharp
TT.CheckFollowAwemeState(
    success: (result) =>
    {
        if (result.HasFollowed)
        {
            Debug.Log("用户已关注该抖音号");
        }
        else
        {
            Debug.Log("用户未关注，可引导关注");
        }
    },
    fail: (error) => Debug.Log($"查询失败: {error.ErrMsg}")
);
```

---

### 4.2 TT.OpenAwemeUserProfile

**说明**: 打开指定抖音号的用户主页。

**语法**:

```csharp
public static void OpenAwemeUserProfile(string awemeId = null, Action success = null, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| awemeId | string | 否 | null | 抖音号 ID，不传则打开游戏绑定账号的主页 |
| success | Action | 否 | null | 打开成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 打开失败回调 |

**代码示例**:

```csharp
// 打开游戏绑定的官方抖音号主页
TT.OpenAwemeUserProfile(
    success: () => Debug.Log("已打开主页"),
    fail: (error) => Debug.Log($"打开失败: {error.ErrMsg}")
);

// 打开指定抖音号主页
TT.OpenAwemeUserProfile("aweme_xxxxx",
    success: () => Debug.Log("已打开指定抖音号主页")
);
```

---

### 4.3 TT.CheckBoundAweme

**说明**: 检查当前游戏是否绑定了抖音号。

**语法**:

```csharp
public static void CheckBoundAweme(Action<BoundAwemeResult> success, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| success | Action\<BoundAwemeResult\> | 是 | - | 成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 失败回调 |

**代码示例**:

```csharp
TT.CheckBoundAweme(
    success: (result) =>
    {
        // ⚠️ 安全：抖音号 ID 为永久用户标识，生产环境禁止打印
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"是否绑定: {result.IsBound}");
        Debug.Log($"绑定抖音号ID: {result.AwemeId}");
        #else
        Debug.Log($"是否绑定: {result.IsBound}");
        #endif
    },
    fail: (error) => Debug.Log($"查询失败: {error.ErrMsg}")
);
```

---

## 五、直玩（推荐流直出游戏）

直玩能力允许用户在抖音推荐流中直接试玩游戏，无需下载安装。

### 5.1 TT.RequestFeedSubscribe

**说明**: 请求用户订阅推荐流直出游戏，订阅后用户可在推荐流中直接启动游戏。

**语法**:

```csharp
public static void RequestFeedSubscribe(Action success = null, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| success | Action | 否 | null | 订阅成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 订阅失败回调 |

**代码示例**:

```csharp
TT.RequestFeedSubscribe(
    success: () => Debug.Log("直玩订阅成功"),
    fail: (error) => Debug.Log($"直玩订阅失败: {error.ErrMsg}")
);
```

---

### 5.2 TT.CheckFeedSubscribeStatus

**说明**: 检查用户当前直玩订阅状态。

**语法**:

```csharp
public static void CheckFeedSubscribeStatus(Action<FeedSubscribeResult> success, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| success | Action\<FeedSubscribeResult\> | 是 | - | 成功回调，返回订阅状态 |
| fail | Action\<ErrorInfo\> | 否 | null | 失败回调 |

**代码示例**:

```csharp
TT.CheckFeedSubscribeStatus(
    success: (result) =>
    {
        if (result.IsSubscribed)
        {
            Debug.Log("用户已订阅直玩");
        }
        else
        {
            Debug.Log("用户未订阅直玩");
            TT.RequestFeedSubscribe(); // 引导订阅
        }
    },
    fail: (error) => Debug.Log($"查询失败: {error.ErrMsg}")
);
```

---

### 5.3 TT.OnFeedStatusChange

**说明**: 监听推荐流直出游戏的状态变化事件。

**语法**:

```csharp
public static void OnFeedStatusChange(Action<FeedStatusChangeEvent> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| callback | Action\<FeedStatusChangeEvent\> | 是 | - | 状态变化回调 |

**代码示例**:

```csharp
TT.OnFeedStatusChange((eventData) =>
{
    Debug.Log($"直玩状态变化: {eventData.Status}");
    switch (eventData.Status)
    {
        case "playing":
            Debug.Log("用户在推荐流中开始游戏");
            break;
        case "paused":
            Debug.Log("用户在推荐流中暂停游戏");
            break;
        case "closed":
            Debug.Log("用户关闭推荐流游戏");
            break;
    }
});
```

---

### 5.4 TT.OffFeedStatusChange

**说明**: 取消监听推荐流直出游戏的状态变化事件。

**语法**:

```csharp
public static void OffFeedStatusChange(Action<FeedStatusChangeEvent> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| callback | Action\<FeedStatusChangeEvent\> | 是 | - | 需移除的监听回调 |

**代码示例**:

```csharp
// 注册监听
private Action<FeedStatusChangeEvent> onFeedChange;

void OnEnable()
{
    onFeedChange = (eventData) => Debug.Log($"直玩状态: {eventData.Status}");
    TT.OnFeedStatusChange(onFeedChange);
}

void OnDisable()
{
    // 取消监听，避免内存泄漏
    TT.OffFeedStatusChange(onFeedChange);
}
```

---

## 六、游戏互推

### 6.1 TT.CreateGridGamePanel

**说明**: 创建游戏互推面板，在指定区域展示其他推荐游戏的网格列表。

**语法**:

```csharp
public static GridGamePanel CreateGridGamePanel(GridGamePanelParam param)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| param | GridGamePanelParam | 是 | - | 互推面板参数对象 |

**GridGamePanelParam 属性**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| X | float | 否 | 0 | 面板 X 坐标（Unity 世界坐标） |
| Y | float | 否 | 0 | 面板 Y 坐标（Unity 世界坐标） |
| Width | float | 否 | 300 | 面板宽度 |
| Height | float | 否 | 400 | 面板高度 |
| ColumnCount | int | 否 | 2 | 网格列数 |

**GridGamePanel 对象方法**:

| 方法 | 说明 |
|------|------|
| Show() | 显示互推面板 |
| Hide() | 隐藏互推面板 |
| Destroy() | 销毁互推面板，释放资源 |
| OnShow(Action callback) | 面板显示事件 |
| OnHide(Action callback) | 面板隐藏事件 |

**代码示例**:

```csharp
// 创建互推面板
var panelParam = new GridGamePanelParam
{
    X = 50,
    Y = 100,
    Width = 600,
    Height = 800,
    ColumnCount = 3
};

var gamePanel = TT.CreateGridGamePanel(panelParam);

gamePanel.OnShow(() => Debug.Log("互推面板已显示"));
gamePanel.OnHide(() => Debug.Log("互推面板已隐藏"));

// 显示面板
gamePanel.Show();

// 在适当时机隐藏
// gamePanel.Hide();

// 销毁时释放资源
// gamePanel.Destroy();
```

---

## 七、游戏排行榜

### 7.1 TT.SetImRankData

**说明**: 设置用户在当前群的 IM 排行榜数据，用于群排行榜功能。

**语法**:

```csharp
public static void SetImRankData(ImRankDataParam param, Action success = null, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| param | ImRankDataParam | 是 | - | 排行榜数据参数 |
| success | Action | 否 | null | 设置成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 设置失败回调 |

**ImRankDataParam 属性**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| Score | int | 是 | - | 排行榜分数 |
| RankData | string | 否 | "" | 额外排名数据（JSON 字符串） |

**代码示例**:

```csharp
var rankParam = new ImRankDataParam
{
    Score = 9999,
    RankData = "{\"level\":50,\"title\":\"王者\"}"
};

TT.SetImRankData(rankParam,
    success: () => Debug.Log("排行榜数据更新成功"),
    fail: (error) => Debug.Log($"更新失败: {error.ErrMsg}")
);
```

---

### 7.2 TT.GetImRankList

**说明**: 获取当前群的 IM 排行榜列表。

**语法**:

```csharp
public static void GetImRankList(Action<ImRankListResult> success, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| success | Action\<ImRankListResult\> | 是 | - | 成功回调，返回排行榜列表 |
| fail | Action\<ErrorInfo\> | 否 | null | 失败回调 |

**代码示例**:

```csharp
TT.GetImRankList(
    success: (result) =>
    {
        Debug.Log($"排行榜列表长度: {result.RankList.Length}");
        foreach (var item in result.RankList)
        {
            Debug.Log($"第{item.Rank}名: {item.NickName} - 分数:{item.Score}");
        }
    },
    fail: (error) => Debug.Log($"获取排行榜失败: {error.ErrMsg}")
);
```

---

### 7.3 TT.GetImRankData

**说明**: 获取当前用户在群排行榜中的个人排名数据。

**语法**:

```csharp
public static void GetImRankData(Action<ImRankDataResult> success, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| success | Action\<ImRankDataResult\> | 是 | - | 成功回调，返回个人排名 |
| fail | Action\<ErrorInfo\> | 否 | null | 失败回调 |

**代码示例**:

```csharp
TT.GetImRankData(
    success: (result) =>
    {
        Debug.Log($"我的排名: 第{result.Rank}名");
        Debug.Log($"我的分数: {result.Score}");
    },
    fail: (error) => Debug.Log($"获取个人排名失败: {error.ErrMsg}")
);
```

---

## 八、直播能力

### 8.1 TT.GetLiveManager

**说明**: 获取直播管理器实例，用于与抖音直播进行交互。

**语法**:

```csharp
public static TTLiveManager GetLiveManager()
```

**返回值**:

| 类型 | 说明 |
|------|------|
| TTLiveManager | 直播管理器单例实例 |

**TTLiveManager 方法**:

#### CheckRoomIsValid

**说明**: 检查直播间是否可用。

```csharp
public void CheckRoomIsValid(Action<bool> callback)
```

#### GetLiveStatus

**说明**: 获取当前直播状态。

```csharp
public void GetLiveStatus(Action<LiveStatusResult> callback)
```

#### NavigateToLive

**说明**: 导航到指定直播间。

```csharp
public void NavigateToLive(string roomId, Action success = null, Action<ErrorInfo> fail = null)
```

#### OnXScreenSizeChange

**说明**: 监听异形屏尺寸变化（如直播小窗模式）。

```csharp
public void OnXScreenSizeChange(Action<XScreenSizeEvent> callback)
```

#### OffXScreenSizeChange

**说明**: 取消监听异形屏尺寸变化。

```csharp
public void OffXScreenSizeChange(Action<XScreenSizeEvent> callback)
```

**代码示例**:

```csharp
var liveManager = TT.GetLiveManager();

// 检查直播间是否可用
liveManager.CheckRoomIsValid((isValid) =>
{
    if (isValid)
    {
        Debug.Log("直播间可用");
    }
    else
    {
        Debug.Log("当前不在直播间或直播能力不可用");
    }
});

// 获取直播状态
liveManager.GetLiveStatus((status) =>
{
    Debug.Log($"直播状态: {status.Status}");
    Debug.Log($"直播间ID: {status.RoomId}");
    Debug.Log($"是否正在直播: {status.IsLiving}");
});

// 导航到直播间
liveManager.NavigateToLive("room_xxxxx",
    success: () => Debug.Log("已跳转到直播间"),
    fail: (error) => Debug.Log($"跳转失败: {error.ErrMsg}")
);

// 监听异形屏变化
liveManager.OnXScreenSizeChange((eventData) =>
{
    Debug.Log($"屏幕尺寸变化: width={eventData.Width}, height={eventData.Height}");
    Debug.Log($"安全区域: top={eventData.SafeAreaTop}, bottom={eventData.SafeAreaBottom}");
    // 适配 UI 布局
});
```

---

## 九、公会群

### 9.1 TT.GetUnionGroupInfo

**说明**: 获取公会群的基本信息。

**语法**:

```csharp
public static void GetUnionGroupInfo(Action<UnionGroupInfoResult> success, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| success | Action\<UnionGroupInfoResult\> | 是 | - | 成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 失败回调 |

**代码示例**:

```csharp
TT.GetUnionGroupInfo(
    success: (info) =>
    {
        Debug.Log($"公会群ID: {info.GroupId}");
        Debug.Log($"公会群名称: {info.GroupName}");
        Debug.Log($"是否已绑定: {info.IsBound}");
    },
    fail: (error) => Debug.Log($"获取公会群信息失败: {error.ErrMsg}")
);
```

---

### 9.2 TT.BindUnionGroup

**说明**: 绑定游戏与公会群的关联关系。

**语法**:

```csharp
public static void BindUnionGroup(string groupId, Action success = null, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| groupId | string | 是 | - | 公会群 ID |
| success | Action | 否 | null | 绑定成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 绑定失败回调 |

**代码示例**:

```csharp
TT.BindUnionGroup("union_group_xxxxx",
    success: () => Debug.Log("公会群绑定成功"),
    fail: (error) => Debug.Log($"绑定失败: {error.ErrMsg} ({error.ErrorCode})")
);
```

---

### 9.3 TT.UnbindUnionGroup

**说明**: 解绑游戏与公会群的关联关系。

**语法**:

```csharp
public static void UnbindUnionGroup(string groupId, Action success = null, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| groupId | string | 是 | - | 公会群 ID |
| success | Action | 否 | null | 解绑成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 解绑失败回调 |

**代码示例**:

```csharp
TT.UnbindUnionGroup("union_group_xxxxx",
    success: () => Debug.Log("公会群解绑成功"),
    fail: (error) => Debug.Log($"解绑失败: {error.ErrMsg}")
);
```

---

### 9.4 TT.JoinUnionGroup

**说明**: 引导用户加入公会群。

**语法**:

```csharp
public static void JoinUnionGroup(string groupId, Action success = null, Action<ErrorInfo> fail = null, Action complete = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| groupId | string | 是 | - | 公会群 ID |
| success | Action | 否 | null | 加入成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 加入失败回调 |
| complete | Action | 否 | null | 操作完成回调 |

**代码示例**:

```csharp
TT.JoinUnionGroup("union_group_xxxxx",
    success: () => Debug.Log("已加入公会群"),
    fail: (error) => Debug.Log($"加入失败: {error.ErrMsg}"),
    complete: () => Debug.Log("入群流程结束")
);
```

---

## 十、订阅消息

### 10.1 TT.RequestSubscribeMessage

**说明**: 请求用户授权订阅消息（模板消息），授权后可向用户发送服务通知。

**语法**:

```csharp
public static void RequestSubscribeMessage(string[] tmplIds, Action<SubscribeMessageResult> success, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| tmplIds | string[] | 是 | - | 需要订阅的消息模板 ID 列表 |
| success | Action\<SubscribeMessageResult\> | 是 | - | 授权成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 授权失败回调 |

**代码示例**:

```csharp
string[] templateIds = new string[] { "tmpl_001", "tmpl_002", "tmpl_003" };

TT.RequestSubscribeMessage(templateIds,
    success: (result) =>
    {
        foreach (var item in result.SubscribeResults)
        {
            Debug.Log($"模板 {item.TmplId}: {(item.Accepted ? "已订阅" : "已拒绝")}");
        }
    },
    fail: (error) => Debug.Log($"订阅失败: {error.ErrMsg}")
);
```

---

## 十一、数据分析

### 11.1 TT.ReportAnalytics

**说明**: 上报自定义分析事件，用于抖音开发者平台的数据统计。

**语法**:

```csharp
public static void ReportAnalytics(string eventName, string eventData = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| eventName | string | 是 | - | 事件名称，需在开发者平台预先配置 |
| eventData | string | 否 | null | 事件参数（JSON 字符串） |

**代码示例**:

> ⚠️ **【隐私合规提示】**：`ReportAnalytics` 上报的数据会关联用户身份。建议：
> - 在用户首次登录时展示隐私政策并征得同意后启用数据分析上报
> - `eventData` 中不得包含 `openid`、`code`、`session_key` 等敏感凭证
> - 涉及用户行为的精细化分析（如关卡耗时）应在隐私政策中明确披露用途

```csharp
// 上报关卡通过事件
TT.ReportAnalytics("level_complete", "{\"levelId\":5,\"score\":12500,\"duration\":180}");

// 上报购买事件
TT.ReportAnalytics("item_purchase", "{\"itemId\":\"weapon_001\",\"price\":6,\"currency\":\"CNY\"}");

// 上报自定义事件（无额外数据）
TT.ReportAnalytics("daily_login");
```

---

### 11.2 TT.ReportScene

**说明**: 上报场景切换事件，用于分析用户在游戏中的行为路径。

**语法**:

```csharp
public static void ReportScene(string sceneId, int costTime = 0, string extraData = null, Action success = null, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| sceneId | string | 是 | - | 场景 ID |
| costTime | int | 否 | 0 | 场景耗时（毫秒） |
| extraData | string | 否 | null | 额外数据（JSON） |
| success | Action | 否 | null | 上报成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 上报失败回调 |

**代码示例**:

> ⚠️ **【隐私合规提示】**：`ReportScene` 上报场景切换数据会关联用户身份。建议在隐私政策中披露场景数据采集用途，并在首次调用前获取用户同意。

```csharp
// 上报场景切换
TT.ReportScene("main_menu", 0, null,
    success: () => Debug.Log("场景上报成功")
);

// 上报场景带耗时
TT.ReportScene("battle_scene", 2500, "{\"enemyCount\":10}",
    success: () => Debug.Log("战斗场景上报成功"),
    fail: (error) => Debug.Log($"场景上报失败: {error.ErrMsg}")
);
```

---

## 十二、客服

### 12.1 TT.OpenCustomerServiceConversation

**说明**: 打开客服会话页面，用户可与开发者进行沟通。

**语法**:

```csharp
public static void OpenCustomerServiceConversation(Action success = null, Action<ErrorInfo> fail = null)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| success | Action | 否 | null | 打开成功回调 |
| fail | Action\<ErrorInfo\> | 否 | null | 打开失败回调 |

**代码示例**:

```csharp
TT.OpenCustomerServiceConversation(
    success: () => Debug.Log("客服会话已打开"),
    fail: (error) => Debug.Log($"打开客服失败: {error.ErrMsg}")
);
```

---

### 12.2 TT.OpenAwemeCustomerService

**说明**: 打开抖音号客服页面（即钻石支付客服页面），可同时用于客服咨询和钻石支付。

**语法**:

```csharp
public static void OpenAwemeCustomerService(OpenAwemeCustomerServiceParam param)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| param | OpenAwemeCustomerServiceParam | 是 | - | 客服/支付参数对象 |

> 详细参数定义及支付流程见 [unity-payment.md](unity-payment.md) 第一节。

**代码示例**:

```csharp
// 仅打开客服咨询（不涉及支付）
var param = new OpenAwemeCustomerServiceParam
{
    Success = () => Debug.Log("客服页面已关闭"),
    Fail = (error) => Debug.Log($"打开失败: {error.ErrMsg}")
};
TT.OpenAwemeCustomerService(param);
```

---

## 十三、快捷方式

### 13.1 TT.AddShortcut

**说明**: 提示用户添加游戏快捷方式到桌面。

**语法**:

```csharp
public static void AddShortcut(Action<bool> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| callback | Action\<bool\> | 是 | - | 回调，参数为 true 表示添加成功 |

**代码示例**:

```csharp
TT.AddShortcut((success) =>
{
    if (success)
    {
        Debug.Log("快捷方式已添加到桌面");
    }
    else
    {
        Debug.Log("用户取消添加或操作失败");
    }
});
```

---

### 13.2 TT.CheckShortcut

**说明**: 检查是否已存在游戏快捷方式。

**语法**:

```csharp
public static void CheckShortcut(Action<bool> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| callback | Action\<bool\> | 是 | - | 回调，参数为 true 表示快捷方式已存在 |

**代码示例**:

```csharp
TT.CheckShortcut((exists) =>
{
    if (!exists)
    {
        Debug.Log("快捷方式不存在，弹出引导");
        TT.AddShortcut((success) => Debug.Log($"添加结果: {success}"));
    }
    else
    {
        Debug.Log("快捷方式已存在");
    }
});
```

---

## 十四、邀请模块

### 14.1 TT.CreateInvitePanel

**说明**: 创建游戏邀请面板，用户可通过该面板邀请好友一起游戏。

**语法**:

```csharp
public static InvitePanel CreateInvitePanel(InvitePanelParam param)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| param | InvitePanelParam | 是 | - | 邀请面板参数对象 |

**InvitePanelParam 属性**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| RoomId | string | 否 | "" | 房间 ID，透传给被邀请方 |
| Query | string | 否 | "" | 自定义参数，透传给被邀请方 |
| Timeout | int | 否 | 30000 | 邀请超时时间（毫秒） |

**InvitePanel 对象方法**:

| 方法 | 说明 |
|------|------|
| Show() | 显示邀请面板 |
| Hide() | 隐藏邀请面板 |
| Destroy() | 销毁邀请面板 |
| OnSuccess(Action\<InviteResult\> callback) | 邀请成功回调 |
| OnFail(Action\<ErrorInfo\> callback) | 邀请失败回调 |

**代码示例**:

```csharp
var inviteParam = new InvitePanelParam
{
    RoomId = "room_12345",
    Query = "mode=ranked&map=forest",
    Timeout = 30000
};

var invitePanel = TT.CreateInvitePanel(inviteParam);

invitePanel.OnSuccess((result) =>
{
    Debug.Log($"邀请成功: 已邀请 {result.InvitedCount} 位好友");
});

invitePanel.OnFail((error) =>
{
    Debug.Log($"邀请失败: {error.ErrMsg} ({error.ErrorCode})");
});

invitePanel.Show();
```

---

### 14.2 TT.OnInviteStateChanged

**说明**: 监听好友邀请状态变化（作为被邀请方时使用）。

**语法**:

```csharp
public static void OnInviteStateChanged(Action<InviteStateEvent> callback)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| callback | Action\<InviteStateEvent\> | 是 | - | 邀请状态变化回调 |

**代码示例**:

```csharp
TT.OnInviteStateChanged((eventData) =>
{
    // ⚠️ 安全：OpenId 为永久用户标识，生产环境禁止打印
    #if UNITY_EDITOR || DEVELOPMENT_BUILD
    Debug.Log($"邀请状态: {eventData.State}");
    Debug.Log($"邀请方 openId: {eventData.OpenId}");
    Debug.Log($"房间ID: {eventData.RoomId}");
    Debug.Log($"自定义参数: {eventData.Query}");
    #else
    Debug.Log($"邀请状态: {eventData.State}");
    Debug.Log($"房间ID: {eventData.RoomId}");
    #endif

    switch (eventData.State)
    {
        case "invited":
            Debug.Log("收到好友邀请");
            // 可选择自动加入或展示提示
            break;
        case "accepted":
            Debug.Log("邀请已被接受");
            break;
    }
});
```
