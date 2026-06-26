## aipexbase-js API 快速参考

### 初始化客户端

```javascript
const client = aipexbase.createClient({
  baseUrl: 'http://your-server.com',
  apiKey: 'baas_xxxxxxxxxxxx'
});
```

### 认证模块 (client.auth)

如果应用配置了认证，即可使用登录注册。

#### 注册

```javascript
await client.auth.register({})  // 这里数据结构即是绑定的认证表数据结构
```

#### 登录

需要认证的情况下，注册完成后必须选择以下方式进行登录：

```javascript
// 密码登录（密码登录必须使用user_name、phone、email其中之一，不允许使用其它字段名）
await client.auth.login({ email: 'user@example.com', password: '123456' });
await client.auth.login({ phone: '13800138000', password: '123456' });
await client.auth.login({ user_name: 'user_name', password: '123456' });

// 验证码登录
await client.auth.loginByPhoneAndCode({ phone: '13800138000', code: '123456' });
await client.auth.loginByEmailAndCode({ email: 'user@example.com', code: '123456' });

// 微信登录
await client.auth.loginByWeChat({ code: 'wx_code' });
await client.auth.loginByWeApp({ code: 'weapp_code' });
```

#### 获取当前用户信息

```javascript
const userInfo = await client.auth.getUser();
```

#### 登出

```javascript
await client.auth.logout();
```

### 数据库模块 (client.db)

#### 查询操作

```javascript
// 列表查询
await client.db.from('users').list();

// 带条件查询
await client.db.from('users').list()
  .eq('status', 'active')
  .gt('age', 18)
  .order('created_at', 'desc');

// 分页查询
await client.db.from('users').page()
  .page(1, 20)
  .eq('status', 'active');
// 单条查询
await client.db.from('users').get()
  .eq('id', 'rec_xxx');
```
**返回格式：**
1. list() 列表返回格式:
    ```json
    {
       "code":0,
       "data":[],
       "message":"ok",
       "success":true
   }
    ```

2. page() 分页返回格式:
    ```json
    {
        "code": 0,
        "data": {
            "records": [],
            "total": 0,
            "size": 20,
            "current": 1
        },
        "message": "ok",
        "success": true
    }
    ```
   
3. get() 详情返回格式:
    ```json
    {
        "code": 0,
        "data": {},
        "message": "ok",
        "success": true
    }
    ```

#### 过滤操作符

```javascript
.eq('field', value)              // 等于
.neq('field', value)             // 不等于
.gt('field', value)              // 大于
.gte('field', value)             // 大于等于
.lt('field', value)              // 小于
.lte('field', value)             // 小于等于
.like('field', value)            // 模糊匹配
.in('field', [v1, v2, v3])       // 在列表中
.between('field', [min, max])    // 在区间内
```

#### OR 条件

```javascript
await client.db.from('users').list()
  .eq('status', 'active')
  .or((q) => {
    q.eq('role', 'admin').eq('role', 'moderator');
  });
```

#### 排序

```javascript
.order('created_at', 'asc')      // 升序
.order('created_at', 'desc')     // 降序
```

#### 插入数据

```javascript
await client.db.from('users').insert()
  .values({ name: 'John', email: 'john@example.com', age: 25 });
```

返回格式：

```javascript
{
  "code": 0,
  "success": true,
  "message": "ok",
  "data": 1  // 数据的主键id值
}
```

#### 更新数据

```javascript
await client.db.from('users').update()
  .set({ status: 'inactive' })
  .eq('id', 'rec_xxx');
```

返回格式：

```javascript
{
  "code": 0,
  "success": true,
  "message": "ok",
  "data": 1  // 1-更新成功 0-未更新
}
```

#### 删除数据

```javascript
await client.db.from('users').delete()
  .eq('id', 'rec_xxx');
```

### AI 模块 (client.ai)

```javascript
// 文本对话
await client.ai.chat()
  .text('你好，介绍一下你自己')
  .prompt('你是一个友好的助手')
  .conversationId('session-123');

// 图生文
await client.ai.imageToText()
  .url('https://example.com/image.jpg')
  .text('这张图片里有什么？')
  .prompt('请详细描述');

// 文生图
await client.ai.textToImage()
  .text('一只可爱的熊猫在竹林里');

// 文本转语音
await client.ai.textToSpeech()
  .text('欢迎使用语音合成服务');

// 文本转视频（自动执行）
await client.ai.textToVideo()
  .text('一只小猫在草地上玩耍');

// 文本转音频（自动执行）
await client.ai.textToAudio()
  .prompt('一段优美的旋律');

// 即梦文生图
await client.ai.jmTextToImage()
  .prompt('可爱的小猫')
  .scale(0.5);

// 即梦生成视频
await client.ai.jmGenToVideo()
  .prompt('视频描述')
  .image('https://example.com/image.jpg');
```

### API 模块 (client.api)

```javascript
// 调用自定义 API
await client.api.call('yourApiName')
  .param('key1', 'value1')
  .param('key2', 'value2');

// 批量设置参数
await client.api.call('yourApiName')
  .params({ key1: 'value1', key2: 'value2' });

// 自定义请求头
await client.api.call('yourApiName')
  .headers({ 'X-Custom-Header': 'value' })
  .params({ data: 'value' });
```

### 其他模块

#### 物流查询

```javascript
await client.logistics.trackPackage()
  .company('yuantong')
  .trackingNumber('123456789')
  .track();

// 顺丰需要手机号
await client.logistics.trackPackage()
  .company('shunfeng')
  .trackingNumber('SF123456789')
  .phone('13800138000')
  .track();
```

#### 地理位置

```javascript
// 经纬度转地址
await client.location.locationToAddress()
  .latitude(39.9042)
  .longitude(116.4074);

// 地址转经纬度
await client.location.addressToLocation()
  .address('北京市天安门广场');

// 路线规划
await client.location.driving()
  .from(39.9042, 116.4074)
  .to(40.0076, 116.4929);

// 附近搜索
await client.location.nearby()
  .lat(39.9042)
  .lng(116.4074)
  .radius(1000)
  .keyword('餐厅');
```

#### 通知模块

```javascript
// 飞书机器人
await client.notification.feishuRobot()
  .content('消息内容');

// 企业微信机器人
await client.notification.wechatRobot()
  .content('消息内容');

// 邮件发送
await client.notification.mail()
  .to('user@example.com')
  .title('邮件标题')
  .content('邮件内容')
  .params({ username: 'John', code: 'ABC123' });
```

### 返回数据格式

所有 API 返回格式统一：

```javascript
{
  "code": 0,
  "success": true,
  "message": "ok",
  "data": { ... }  // 实际数据
}
```

### 错误处理

```javascript
try {
  const result = await client.db.from('users').list();
  if (result.success) {
    // 处理成功
    console.log(result.data);
  } else {
    // 处理失败
    console.error(result.message);
  }
} catch (error) {
  // 处理异常
  console.error(error.message);
}
```

---

# 前端开发注意事项
不限技术栈（纯 HTML/Vue/React 等），默认使用纯 HTML，所有文件放到项目目录下。

### SDK 引入（CDN 方式）

```html
<script src="https://cdn.jsdelivr.net/npm/aipexbase-js/dist/aipexbase.umd.min.js"></script>
```

### 客户端初始化（必须严格按此方式）

```javascript
const client = aipexbase.createClient({
    baseUrl: '<从 baas-config.json 读取 baseUrl>',
    apiKey: '<从 baas-config.json 读取 apiKey>'
});
```

> **禁止** 使用 `new AipexBase()`、`new AipexbaseClient()` 或任何其他初始化方式。唯一正确的方式是 `aipexbase.createClient({ baseUrl, apiKey })`。

### 必填字段处理

根据 `app-schema.json` 中的 `isNullable` 字段判断是否必填（`isNullable: true` 为必填）。前端表单中：

- 必填字段的 label 旁必须显示红色星号 `*` 标识（如 `<span class="text-red-500">*</span>`）
- 必填字段的 input 必须添加 `required` 属性
- 提交表单时必须校验所有必填字段，未填写时给出提示
- **datetime 类型字段例外**：datetime 字段的 `isNullable` 在 schema 中必须为 `false`（非必填），因此前端表单中 datetime 字段不显示红色星号、不添加 `required` 属性、提交时不做必填校验

### 表单字段渲染强制规则（新增/编辑页面）

- 新增和编辑表单的字段列表必须来源于 `app-schema.json`，禁止手写一部分字段后遗漏其余字段
- 所有 `isNullable: true` 的必填字段，必须在表单中可见、可输入、可提交，严禁漏渲染
- 若字段不应由用户输入（如自增主键 `id`），可不渲染输入框，但其余业务必填字段必须展示
- 提交前必须做"字段完整性检查"：逐一比对 schema 必填字段与页面已渲染字段，缺一不可提交
- 若是多步骤表单，也必须确保所有必填字段在某个步骤中出现并被校验

#### 新增/编辑页自检清单（提交前必查）

- [ ] `app-schema.json` 中每个 `isNullable: true` 的字段都在表单中有对应输入项（自增主键除外）
- [ ] 每个必填输入项都带 `required` 或等价前端校验规则
- [ ] 缺少任一必填字段时，页面会阻止提交并提示具体字段名

### 认证流程强制规则（needAuth: true 时必须遵守）

- 登录成功后，**必须立即调用 `client.auth.getUser()` 获取当前用户的完整信息**，用返回的用户数据作为 `currentUser`，禁止直接使用 `login()` 返回的 `res.data` 作为用户信息展示
- 页面加载时，应先调用 `client.auth.getUser()` 检查是否已登录，若已登录则直接进入主页面，无需重新登录
- 用户名、角色等展示信息必须来自 `getUser()` 的返回值，确保与数据库一致
- 登录和自动登录（页面刷新恢复会话）应共用同一个"进入主页面"逻辑，避免代码重复导致展示不一致

### 图片/文件上传强制规则

- `app-schema.json` 中字段类型为图片URL（如封面图 `cover`）或 `columnComment` 含"图片"的字段，前端**必须提供文件上传组件**（`<input type="file">`），**严禁**使用纯文本输入框让用户手动填写 URL
- 上传时应显示加载状态，上传成功后显示图片预览
- token 获取方式：`localStorage.getItem('baas_token')`（SDK 登录后自动存储）
- 上传文件示例：
```
                const response = await fetch('<baseUrl>/common/upload', {
                    method: 'POST',
                    headers: {
                        'CODE_FLYING': '<此处填写apiKey，从 baas-config.json 读取 apiKey>'
                    },
                    body: formData
                });

                const result = await response.json();
                if (result.success && result.data) {
                    callback(result.data.url);
                } else {
                    showToast('上传失败', 'error');
                }
```

### 其它事项
- **严禁凭记忆或猜测编写 API 调用代码**。方法链的调用顺序、参数传递方式必须与 `aipexbase-js-api.md` 中的示例完全一致。
- 实现业务逻辑，**数据库操作必须使用 `client.db` 模块**
- **⚠️ 禁止** 使用 `client.from()`、`client.select()` 等不存在的 API。所有数据库操作必须通过 `client.db.from('表名')` 开始，后接 `.list()` / `.get()` / `.page()` / `.insert()` / `.update()` / `.delete()` 等方法。
- **⚠️ 删除和更新操作必须携带条件**：`.update()` 和 `.delete()` 调用时必须附带 `.eq()` 等条件方法指定目标记录，**严禁**执行无条件的更新或删除，防止误操作影响全表数据。

---

## 平台扩展能力模块

除数据库和认证外，SDK 还提供以下能力模块，设计需求文档时应了解这些可用能力，合理利用。

### AI 模块 (client.ai)

```javascript
// 文本对话
await client.ai.chat()
  .text('你好，介绍一下你自己')
  .prompt('你是一个友好的助手')
  .conversationId('session-123');

// 图生文
await client.ai.imageToText()
  .url('https://example.com/image.jpg')
  .text('这张图片里有什么？')
  .prompt('请详细描述');

// 文生图
await client.ai.textToImage()
  .text('一只可爱的熊猫在竹林里');

// 文本转语音
await client.ai.textToSpeech()
  .text('欢迎使用语音合成服务');

// 文本转视频（自动执行）
await client.ai.textToVideo()
  .text('一只小猫在草地上玩耍');

// 文本转音频（自动执行）
await client.ai.textToAudio()
  .prompt('一段优美的旋律');

// 即梦文生图
await client.ai.jmTextToImage()
  .prompt('可爱的小猫')
  .scale(0.5);

// 即梦生成视频
await client.ai.jmGenToVideo()
  .prompt('视频描述')
  .image('https://example.com/image.jpg');
```

### API 模块 (client.api)

```javascript
// 调用自定义 API
await client.api.call('yourApiName')
  .param('key1', 'value1')
  .param('key2', 'value2');

// 批量设置参数
await client.api.call('yourApiName')
  .params({ key1: 'value1', key2: 'value2' });

// 自定义请求头
await client.api.call('yourApiName')
  .headers({ 'X-Custom-Header': 'value' })
  .params({ data: 'value' });
```

### 物流查询模块 (client.logistics)

```javascript
await client.logistics.trackPackage()
  .company('yuantong')
  .trackingNumber('123456789')
  .track();

// 顺丰需要手机号
await client.logistics.trackPackage()
  .company('shunfeng')
  .trackingNumber('SF123456789')
  .phone('13800138000')
  .track();
```

### 地理位置模块 (client.location)

```javascript
// 经纬度转地址
await client.location.locationToAddress()
  .latitude(39.9042)
  .longitude(116.4074);

// 地址转经纬度
await client.location.addressToLocation()
  .address('北京市天安门广场');

// 路线规划
await client.location.driving()
  .from(39.9042, 116.4074)
  .to(40.0076, 116.4929);

// 附近搜索
await client.location.nearby()
  .lat(39.9042)
  .lng(116.4074)
  .radius(1000)
  .keyword('餐厅');
```

### 通知模块 (client.notification)

```javascript
// 飞书机器人
await client.notification.feishuRobot()
  .content('消息内容');

// 企业微信机器人
await client.notification.wechatRobot()
  .content('消息内容');

// 邮件发送
await client.notification.mail()
  .to('user@example.com')
  .title('邮件标题')
  .content('邮件内容')
  .params({ username: 'John', code: 'ABC123' });
```