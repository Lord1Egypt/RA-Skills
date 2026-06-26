# 使用示例 | Usage Examples

## 场景 1：寻找团购达人并发送私信

```bash
# 1. 打开抖音搜索"省钱团购"
browser action=open profile=openclaw targetUrl="https://www.douyin.com/jingxuan/search/省钱团购?type=user"

# 2. 等待页面加载
browser action=act request={"kind": "wait", "timeMs": 2000}

# 3. 获取快照
browser action=snapshot

# 4. 分析快照，找到粉丝<2000 的达人
# 从响应中找到类似这样的条目：
# link "省钱团购 关注 抖音号:xxx 2906 获赞 430 粉丝" [ref=e890]

# 5. 点击达人主页
browser action=act request={"kind": "click", "ref": "e890"}

# 6. 等待主页加载
browser action=act request={"kind": "wait", "timeMs": 2000}

# 7. 获取主页快照，确认达人信息
browser action=snapshot

# 8. 点击私信按钮
browser action=act request={"kind": "click", "ref": "e316"}

# 9. 输入消息（根据达人内容选择模板）
# 示例：达人发了面霜笔记 → 用模板1（点赞切入）
browser action=act request={
  "kind": "evaluate",
  "fn": "() => {
    const input = document.querySelector('[contenteditable=\"true\"]');
    input.focus();
    input.textContent = '嗨～看到你笔记里分享的那款面霜，看起来很不错！我这边有个省钱团购群，专门组织大家拼单购买，刚好有你提到的这款，价格能便宜不少，要不要一起呀？👇';
    input.dispatchEvent(new Event('input', {bubbles: true}));
    return 'ok';
  }"
}

# 10. 发送
browser action=act request={
  "kind": "evaluate",
  "fn": "() => {
    const input = document.querySelector('[contenteditable=\"true\"]');
    input.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true}));
    return 'sent';
  }"
}

# 11. 确认发送成功
browser action=snapshot
```

---

## 场景 2：批量拓展（伪代码）

```python
# 关键词列表
keywords = ["省钱团购", "探店", "好物推荐", "美食分享"]

# 筛选条件
criteria = {
  "max_followers": 2000,
  "min_engagement": 3,
  "min_works": 50
}

# 已联系的达人（避免重复）
contacted = set()

for keyword in keywords:
  # 1. 搜索
  open_url(f"https://www.douyin.com/jingxuan/search/{keyword}?type=user")
  wait(2000)
  
  # 2. 获取快照并解析
  snapshot = get_snapshot()
  influencers = parse_influencer_list(snapshot)
  
  # 3. 筛选
  filtered = filter_influencers(influencers, criteria)
  
  # 4. 逐个联系
  for inf in filtered[:5]:  # 每个关键词最多联系 5 个
    if inf.id in contacted:
      continue
    
    # 打开主页
    click(inf.ref)
    wait(2000)
    
    # 获取主页信息
    profile = get_profile_snapshot()
    
    # 定制消息
    message = customize_message(profile)
    
    # 发送私信
    send_dm(message)
    
    # 记录
    log_contact(inf)
    contacted.add(inf.id)
    
    # 避免风控，间隔 30 秒
    wait(30000)
```

---

## 场景 3：定制私信话术

```javascript
// 根据场景选择最佳模板
const scenarios = {
  // 达人发了具体产品笔记
  product_post: (product) => 
    `嗨～看到你笔记里分享的${product}，看起来很不错！我这边有个省钱团购群，专门组织大家拼单购买，刚好有你提到的这款，价格能便宜不少，要不要一起呀？👇`,
  
  // 从评论区找到的人
  from_comment: (video) =>
    `看到你在${video}下的评论～我也是买了很多年，总结了一些靠谱渠道，建了个团购群专门帮大家省钱，想了解的话可以拉你进来看看，不买也没关系！`,
  
  // 不确定对方情况
  unknown: () =>
    `你好，我这边有个省钱团购群，专门帮大家对接品牌团购价，都是官方发货，有需要可以拉你进来看看～`,
  
  // 对方是女性/年轻用户
  female_young: (field) =>
    `姐妹，我看到你对${field}很有研究呀，能不能请教一下～我这边建了个团购群，想找真正需要的朋友一起拼单，你平时有买这类产品的习惯吗？`
};

// 示例：达人发了面霜笔记
const message = scenarios.product_post('那款面霜');
// 输出：嗨～看到你笔记里分享的那款面霜，看起来很不错！我这边有个省钱团购群...

// 示例：从评论区找到的人
const message2 = scenarios.from_comment('精华评测视频');
// 输出：看到你在精华评测视频下的评论～我也是买了很多年...
```

---

## 场景 4：记录达人信息到表格

```markdown
| 日期 | 达人昵称 | 抖音号 | 粉丝 | 获赞 | 作品数 | IP 属地 | 私信内容 | 状态 |
|------|---------|--------|------|------|--------|--------|---------|------|
| 2026-04-26 | 省钱团购 | jinshuihe917 | 430 | 2906 | 168 | 辽宁丹东 | 交流团购经验 | 已发送 |
| 2026-04-26 | 探店小王 | xxx | 1200 | 8500 | 95 | 北京 | 请教拍摄技巧 | 已发送 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

**跟进状态：**
- `已发送` - 私信已发出
- `已读` - 对方已读（需要对方在线）
- `已回复` - 对方回复了
- `已关注` - 对方关注了你
- `无响应` - 7 天无回复

---

## 场景 5：搜索不同类别达人

```bash
# 美食类
https://www.douyin.com/jingxuan/search/美食分享?type=user
https://www.douyin.com/jingxuan/search/吃货?type=user

# 探店类
https://www.douyin.com/jingxuan/search/探店?type=user
https://www.douyin.com/jingxuan/search/餐厅推荐?type=user

# 团购类
https://www.douyin.com/jingxuan/search/团购达人?type=user
https://www.douyin.com/jingxuan/search/省钱攻略?type=user

# 带货类
https://www.douyin.com/jingxuan/search/好物推荐?type=user
https://www.douyin.com/jingxuan/search/种草?type=user

# 本地类（替换城市名）
https://www.douyin.com/jingxuan/search/北京探店?type=user
https://www.douyin.com/jingxuan/search/上海美食?type=user
```

---

## 注意事项

1. **发送频率**：建议每小时不超过 10 条，每天不超过 50 条
2. **消息内容**：避免敏感词（微信、电话、二维码、转账等）
3. **账号安全**：新号建议先养号 1-2 周再开始拓展
4. **回复跟进**：及时回复达人的消息，建立良好关系
5. **记录管理**：用表格或 CRM 记录已联系的达人，避免重复

---

## 效果追踪

**关键指标：**
- 发送数量：每天发送的私信数
- 回复率：回复数 / 发送数（行业平均 10-30%）
- 关注转化率：关注数 / 发送数
- 合作转化率：达成合作数 / 发送数

**优化方向：**
- 测试不同话术的回复率
- 分析高回复率达人的共同特征
- 调整筛选条件（粉丝区间、互动率等）
- 优化发送时间（工作日 vs 周末、白天 vs 晚上）
