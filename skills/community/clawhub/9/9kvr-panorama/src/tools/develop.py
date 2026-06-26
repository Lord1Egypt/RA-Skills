"""Develop 工具类

提供小程序、网页、现有项目接入全景的开发指导
"""

from typing import Any, Dict, List


class DevelopTools:
    """Develop 工具类"""

    def __init__(self):
        """初始化 Develop 工具"""
        pass

    def getTools(self) -> List[Dict[str, Any]]:
        """获取所有工具定义

        Returns:
            工具定义列表
        """
        return [
            {
                "name": "get_miniprogram_guide",
                "description": "获取小程序接入全景的开发指导文档和代码示例。支持微信小程序、抖音小程序、快手小程序等平台。小程序接入方式主要是使用 webview 组件，通过开发者播放链接来展示全景作品。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "description": "平台类型，可选值：wechat（微信小程序）、toutiao（抖音小程序）、kuaishou（快手小程序）。默认为 wechat",
                            "enum": ["wechat", "toutiao", "kuaishou"],
                        },
                        "feature": {
                            "type": "string",
                            "description": "功能类型，可选值：basic（基础接入）、advanced（高级功能）、custom（自定义配置）。默认为 basic",
                            "enum": ["basic", "advanced", "custom"],
                        },
                        "work_id": {
                            "type": "string",
                            "description": "作品ID（可选），如果提供作品ID，会在示例代码中使用该ID",
                        },
                    },
                },
            },
            {
                "name": "get_web_integration_guide",
                "description": "获取网页项目接入全景的指导文档和代码示例。支持 Vue、React、原生 JavaScript 等框架。网页接入方式主要是使用 iframe 嵌入全景链接。**重要提示：**如果使用开发者播放链接（包含秘钥），建议通过 nginx 代理将秘钥放在服务端，避免在前端暴露秘钥。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "framework": {
                            "type": "string",
                            "description": "框架类型，可选值：vue、react、vanilla（原生JS）。默认为 vue",
                            "enum": ["vue", "react", "vanilla"],
                        },
                        "integration_type": {
                            "type": "string",
                            "description": "接入方式，可选值：embed（iframe嵌入）、iframe（同embed）、api（API调用）。默认为 embed",
                            "enum": ["embed", "iframe", "api"],
                        },
                        "work_id": {
                            "type": "string",
                            "description": "作品ID（可选），如果提供作品ID，会在示例代码中使用该ID",
                        },
                    },
                },
            },
            {
                "name": "get_existing_project_guide",
                "description": "获取现有项目接入全景的指导文档。适用于已有网站、APP、CMS系统等需要接入全景功能的场景。提供通用的接入方案和最佳实践。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_type": {
                            "type": "string",
                            "description": "项目类型，可选值：website（网站）、app（移动应用）、cms（内容管理系统）。默认为 website",
                            "enum": ["website", "app", "cms"],
                        },
                        "tech_stack": {
                            "type": "string",
                            "description": "技术栈（可选），例如：vue2、vue3、react、angular、jquery 等",
                        },
                        "work_id": {
                            "type": "string",
                            "description": "作品ID（可选），如果提供作品ID，会在示例代码中使用该ID",
                        },
                    },
                },
            },
            {
                "name": "generate_integration_code",
                "description": "根据参数生成具体的接入代码示例。可以生成小程序、网页、现有项目的接入代码，支持自定义配置。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "description": "接入类型，必填。可选值：miniprogram（小程序）、web（网页）、existing（现有项目）",
                            "enum": ["miniprogram", "web", "existing"],
                        },
                        "platform": {
                            "type": "string",
                            "description": "平台类型（小程序必填），可选值：wechat、toutiao、kuaishou",
                            "enum": ["wechat", "toutiao", "kuaishou"],
                        },
                        "framework": {
                            "type": "string",
                            "description": "框架类型（网页/现有项目可选），例如：vue、react、vanilla",
                        },
                        "work_id": {
                            "type": "string",
                            "description": "作品ID（可选），如果提供，会在代码中使用该ID",
                        },
                        "developer_url": {
                            "type": "string",
                            "description": "开发者播放链接（可选），格式：https://develop.9kvr.cn/tour/index?key=TOKEN&id=WORK_ID",
                        },
                        "use_proxy": {
                            "type": "boolean",
                            "description": "是否使用代理（网页接入时），如果为 true，会提供 nginx 代理配置示例",
                        },
                    },
                    "required": ["type"],
                },
            },
        ]

    def hasTool(self, name: str) -> bool:
        """检查是否存在指定的工具

        Args:
            name: 工具名称

        Returns:
            是否存在
        """
        return any(tool["name"] == name for tool in self.getTools())

    async def handleTool(self, name: str, args: Any) -> Dict[str, Any]:
        """处理工具调用

        Args:
            name: 工具名称
            args: 工具参数

        Returns:
            工具返回结果

        Raises:
            ValueError: 未知工具名称
        """
        if name == "get_miniprogram_guide":
            return await self.getMiniprogramGuide(args)
        elif name == "get_web_integration_guide":
            return await self.getWebIntegrationGuide(args)
        elif name == "get_existing_project_guide":
            return await self.getExistingProjectGuide(args)
        elif name == "generate_integration_code":
            return await self.generateIntegrationCode(args)
        else:
            raise ValueError(f"Unknown tool: {name}")

    async def getMiniprogramGuide(self, args: Any) -> Dict[str, Any]:
        """获取小程序开发指导

        Args:
            args: 包含 platform、feature、work_id 的参数

        Returns:
            Markdown 格式的开发指导文档
        """
        platform = args.get("platform", "wechat") if isinstance(args, dict) else "wechat"
        feature = args.get("feature", "basic") if isinstance(args, dict) else "basic"
        work_id = args.get("work_id", "YOUR_WORK_ID") if isinstance(args, dict) else "YOUR_WORK_ID"

        platform_name = "微信小程序"
        platform_code = "wx"
        webview_component = "<web-view>"

        if platform == "toutiao":
            platform_name = "抖音小程序"
            platform_code = "tt"
            webview_component = "<web-view>"
        elif platform == "kuaishou":
            platform_name = "快手小程序"
            platform_code = "ks"
            webview_component = "<web-view>"

        developer_url = f"https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id={work_id}"

        if feature == "basic":
            guide_content = f"""# {platform_name}接入全景开发指导

## 概述

{platform_name}接入全景主要通过 **webview** 组件来实现，使用开发者播放链接来展示全景作品。

## 前置条件

1. **开通开发者服务**
   - 登录全景平台，进入开发者控制台
   - 生成开发者秘钥（secretKey）
   - 配置小程序 AppID 和允许的平台类型
   - **重要提示：** 开发者秘钥需要在 [开发者工作台](https://9kvr.cn/user/develop/workbench) 获取

2. **获取开发者播放链接**
   - 格式：`https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id=WORK_ID`
   - 其中 `YOUR_SECRET_KEY` 是您的开发者秘钥（请在 [开发者工作台](https://9kvr.cn/user/develop/workbench) 获取）
   - `WORK_ID` 是全景作品的ID

## 基础接入代码

### 方式一：使用 webview 组件（推荐）

在页面中添加 webview 组件：

```xml
<view class="container">
  <{webview_component}
    src="{{panoramaUrl}}"
    bindmessage="handleMessage"
  ></{webview_component}>
</view>
```

在对应的 JS 文件中：

```javascript
Page({{
  data: {{
    panoramaUrl: '{developer_url}'
  }},

  onLoad(options) {{
    // 从页面参数获取作品ID
    const workId = options.id || '{work_id}';
    // 替换为您的开发者秘钥
    const secretKey = 'YOUR_SECRET_KEY';

    this.setData({{
      panoramaUrl: `https://develop.9kvr.cn/tour/index?key=${{secretKey}}&id=${{workId}}`
    }});
  }},

  handleMessage(e) {{
    // 处理来自 webview 的消息
    console.log('收到消息:', e.detail.data);
  }}
}});
```

### 方式二：跳转到全景小程序

如果需要跳转到芊云全景小程序：

```javascript
{platform_code}.{platform_code}.navigateToMiniProgram({{
  appId: 'YOUR_MINIPROGRAM_APP_ID', // 替换为目标小程序 AppID
  path: 'pages/tour/index?id=' + workId,
  extraData: {{
    secretKey: 'YOUR_SECRET_KEY',
    appName: '您的小程序名称'
  }},
  envVersion: 'release',
  success(res) {{
    console.log('打开成功');
  }},
  fail(err) {{
    console.error('打开失败', err);
  }}
}});
```

## 注意事项

1. **webview 配置**
   - 需要在小程序管理后台配置业务域名：`develop.9kvr.cn`
   - 在 `app.json` 中配置 webview 权限

2. **安全提示**
   - **小程序可以使用秘钥**：小程序代码是编译后的，用户无法直接查看源码，因此可以在小程序代码中直接使用开发者秘钥
   - **网页禁止使用秘钥**：网页代码用户可以直接查看，**禁止**在前端代码中使用秘钥，必须使用 nginx 代理
   - **可选方案**：如果担心安全，也可以通过后端接口获取临时链接

3. **性能优化**
   - webview 加载较慢，建议添加加载提示
   - 可以预加载常用作品链接

## 相关链接

- [查看作品详情]({developer_url.replace('YOUR_SECRET_KEY', 'YOUR_SECRET_KEY')})
- [获取开发者秘钥](https://9kvr.cn/user/develop/workbench) - 在开发者工作台获取您的秘钥
- [查看详细文档](https://9kvr.cn/user/develop/welcome) - 完整的API接口文档和接入指南

### 更多API接口服务

详细文档中提供了以下API接口服务：

- **getVrList()** - 获取全景作品列表，支持分页查询
- **getVrDetail()** - 获取单个全景作品详细信息
- **openWebview()** - 在小程序webview中打开全景链接
- **createVrPanorama()** - 使用API制作VR全景
- **navigateToMiniProgram()** - 小程序跳转打开全景
- **openEmbeddedMiniProgram()** - 芊云全景打开半屏小程序VR
- **embedIframe()** - 使用iframe嵌入全景播放器

更多详细信息请访问：[开发者文档中心](https://9kvr.cn/user/develop/welcome)"""
        elif feature == "advanced":
            guide_content = f"""# {platform_name}高级功能开发指导

## 高级功能

### 1. 与 webview 通信

```javascript
// 向 webview 发送消息
this.selectComponent('#panoramaWebview').postMessage({{
  type: 'control',
  action: 'rotate',
  params: {{ x: 0, y: 90 }}
}});

// 接收 webview 消息
handleMessage(e) {{
  const data = e.detail.data;
  if (data.type === 'sceneChange') {{
    console.log('场景切换:', data.sceneId);
  }}
}}
```

### 2. 自定义导航栏

```javascript
Page({{
  onLoad() {{
    {platform_code}.setNavigationBarTitle({{
      title: '全景作品'
    }});
  }}
}});
```

### 3. 分享功能

```javascript
onShareAppMessage() {{
  return {{
    title: '全景作品分享',
    path: '/pages/tour/index?id=' + this.data.workId,
    imageUrl: '分享图片URL'
  }};
}}
```

## 相关链接

- [获取开发者秘钥](https://9kvr.cn/user/develop/workbench) - 在开发者工作台获取您的秘钥
- [查看详细文档](https://9kvr.cn/user/develop/welcome) - 完整的API接口文档和接入指南

### 更多API接口服务

详细文档中提供了以下API接口服务：

- **getVrList()** - 获取全景作品列表，支持分页查询
- **getVrDetail()** - 获取单个全景作品详细信息
- **openWebview()** - 在小程序webview中打开全景链接
- **createVrPanorama()** - 使用API制作VR全景
- **navigateToMiniProgram()** - 小程序跳转打开全景
- **openEmbeddedMiniProgram()** - 芊云全景打开半屏小程序VR
- **embedIframe()** - 使用iframe嵌入全景播放器

更多详细信息请访问：[开发者文档中心](https://9kvr.cn/user/develop/welcome)"""
        else:
            guide_content = f"""# {platform_name}自定义配置开发指导

## 自定义配置

### 配置 webview 样式

```xml
<{webview_component}
  src="{{panoramaUrl}}"
  style="width: 100%; height: 100vh;"
  bindload="onWebviewLoad"
  binderror="onWebviewError"
></{webview_component}>
```

### 错误处理

```javascript
onWebviewError(e) {{
  console.error('webview 加载失败:', e);
  {platform_code}.showToast({{
    title: '加载失败，请重试',
    icon: 'none'
  }});
}}
```

## 相关链接

- [获取开发者秘钥](https://9kvr.cn/user/develop/workbench) - 在开发者工作台获取您的秘钥
- [查看详细文档](https://9kvr.cn/user/develop/welcome) - 完整的API接口文档和接入指南

### 更多API接口服务

详细文档中提供了以下API接口服务：

- **getVrList()** - 获取全景作品列表，支持分页查询
- **getVrDetail()** - 获取单个全景作品详细信息
- **openWebview()** - 在小程序webview中打开全景链接
- **createVrPanorama()** - 使用API制作VR全景
- **navigateToMiniProgram()** - 小程序跳转打开全景
- **openEmbeddedMiniProgram()** - 芊云全景打开半屏小程序VR
- **embedIframe()** - 使用iframe嵌入全景播放器

更多详细信息请访问：[开发者文档中心](https://9kvr.cn/user/develop/welcome)"""

        return {
            "content": [
                {
                    "type": "text",
                    "text": guide_content,
                },
            ],
        }

    async def getWebIntegrationGuide(self, args: Any) -> Dict[str, Any]:
        """获取网页接入指导

        Args:
            args: 包含 framework、integration_type、work_id 的参数

        Returns:
            Markdown 格式的开发指导文档
        """
        framework = args.get("framework", "vue") if isinstance(args, dict) else "vue"
        work_id = args.get("work_id", "YOUR_WORK_ID") if isinstance(args, dict) else "YOUR_WORK_ID"

        normal_url = f"https://9kvr.cn/tour/index?id={work_id}"
        developer_url = f"https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id={work_id}"

        if framework == "vue":
            guide_content = f"""# Vue 项目接入全景开发指导

## 概述

Vue 项目接入全景主要通过 **iframe** 嵌入全景链接来实现。

## 前置条件

1. **普通接入**：直接使用作品链接，无需秘钥
2. **开发者接入**：需要开通开发者服务，获取开发者播放链接
   - **重要提示：** 开发者秘钥需要在 [开发者工作台](https://9kvr.cn/user/develop/workbench) 获取

## 安全原则

**重要安全提示：**
- 禁止：开发者秘钥不能直接写在前端代码中（会被用户看到）
- 推荐：使用 nginx 代理服务，将秘钥放在服务端
- 最佳实践：通过后端接口获取全景链接，秘钥存储在服务端环境变量中

## 基础接入代码

### 方式一：普通链接接入（推荐新手，无需秘钥）

```vue
<template>
  <div class="panorama-container">
    <iframe
      :src="panoramaUrl"
      frameborder="0"
      style="width: 100%; height: 100vh;"
      allowfullscreen
    ></iframe>
  </div>
</template>

<script>
export default {{
  name: 'PanoramaViewer',
  data() {{
    return {{
      panoramaUrl: '{normal_url}'
    }}
  }},
  mounted() {{
    // 从路由参数获取作品ID
    const workId = this.$route.params.id || '{work_id}';
    // 普通链接无需秘钥
    this.panoramaUrl = `https://9kvr.cn/tour/index?id=${{workId}}`;
  }}
}}
</script>

<style scoped>
.panorama-container {{
  width: 100%;
  height: 100vh;
  overflow: hidden;
}}
</style>
```

### 方式二：开发者链接接入（需要秘钥，强烈建议使用 nginx 代理）

**安全警告：** 开发者链接包含秘钥，**必须**通过 nginx 代理或后端接口获取，**禁止**在前端代码中直接使用秘钥！

#### 前端代码

```vue
<template>
  <div class="panorama-container">
    <iframe
      :src="panoramaUrl"
      frameborder="0"
      style="width: 100%; height: 100vh;"
      allowfullscreen
    ></iframe>
  </div>
</template>

<script>
export default {{
  name: 'PanoramaViewer',
  data() {{
    return {{
      panoramaUrl: ''
    }}
  }},
  async mounted() {{
    const workId = this.$route.params.id || '{work_id}';
    // 通过接口获取代理后的链接（秘钥在服务端）
    const res = await this.$axios.get(`/api/panorama/proxy-url?id=${{workId}}`);
    this.panoramaUrl = res.data.url;
  }}
}}
</script>
```

#### Nginx 代理配置（服务端，强烈推荐）

在您的 nginx 配置文件中添加：

```nginx
# 方案一：返回代理后的链接（前端通过接口获取）
location /api/panorama/proxy-url {{
  # 将秘钥放在服务端，不暴露给前端
  set $secret_key "YOUR_SECRET_KEY";  # 建议从环境变量读取
  set $work_id $arg_id;

  # 返回代理后的链接（前端使用此链接）
  return 200 "https://develop.9kvr.cn/tour/index?key=\\$secret_key&id=\\$work_id";
  add_header Content-Type text/plain;
}}

# 方案二：直接代理整个请求（推荐）
location /panorama/ {{
  proxy_pass https://develop.9kvr.cn/tour/;
  proxy_set_header Host develop.9kvr.cn;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

  # 在代理时添加秘钥参数（秘钥在服务端，前端看不到）
  set $secret_key "YOUR_SECRET_KEY";  # 建议从环境变量读取
  rewrite ^/panorama/(.*)$ /tour/$1?key=$secret_key&$args break;
}}

# 方案三：使用 nginx map 从环境变量读取秘钥（最安全）
map $http_host $panorama_secret {{
  default "YOUR_SECRET_KEY";  # 从环境变量或配置文件读取
}}
location /panorama/ {{
  proxy_pass https://develop.9kvr.cn/tour/;
  proxy_set_header Host develop.9kvr.cn;
  set $secret_key $panorama_secret;
  rewrite ^/panorama/(.*)$ /tour/$1?key=$panorama_secret&$args break;
}}
```

**配置说明：**
- 秘钥存储在 nginx 配置或环境变量中，前端无法获取
- 前端只需访问 `/panorama/index?id=作品ID`，无需知道秘钥
- 建议将秘钥存储在环境变量中，不要硬编码在配置文件中

#### 后端接口示例（Node.js/Express）

```javascript
// 获取代理后的全景链接
app.get('/api/panorama/proxy-url', (req, res) => {{
  const workId = req.query.id;
  const secretKey = process.env.PANORAMA_SECRET_KEY; // 从环境变量读取秘钥
  const url = `https://develop.9kvr.cn/tour/index?key=${{secretKey}}&id=${{workId}}`;
  res.json({{ url }});
}});
```

## 注意事项

1. **安全提示（必须遵守）**
   - 禁止：开发者秘钥不能直接写在前端代码中（会被用户看到）
   - 必须：使用 nginx 代理服务，将秘钥放在服务端
   - 推荐：通过后端接口获取链接，秘钥存储在服务端环境变量中
   - 最佳实践：使用 nginx 直接代理请求，前端无需知道秘钥

2. **iframe 配置**
   - 设置 `allowfullscreen` 属性支持全屏
   - 设置合适的宽高，建议使用 `100vh` 占满视口

3. **响应式设计**
   - 使用 CSS 媒体查询适配移动端
   - 移动端建议使用 `100vw` 和 `100vh`

## 相关链接

- [查看作品]({normal_url})
- [获取开发者秘钥](https://9kvr.cn/user/develop/workbench) - 在开发者工作台获取您的秘钥
- [查看详细文档](https://9kvr.cn/user/develop/welcome) - 完整的API接口文档和接入指南

### 更多API接口服务

详细文档中提供了以下API接口服务：

- **getVrList()** - 获取全景作品列表，支持分页查询
- **getVrDetail()** - 获取单个全景作品详细信息
- **openWebview()** - 在小程序webview中打开全景链接
- **createVrPanorama()** - 使用API制作VR全景
- **navigateToMiniProgram()** - 小程序跳转打开全景
- **openEmbeddedMiniProgram()** - 芊云全景打开半屏小程序VR
- **embedIframe()** - 使用iframe嵌入全景播放器

更多详细信息请访问：[开发者文档中心](https://9kvr.cn/user/develop/welcome)"""
        elif framework == "react":
            guide_content = f"""# React 项目接入全景开发指导

## 概述

React 项目接入全景主要通过 **iframe** 嵌入全景链接来实现。

## 前置条件

1. **普通接入**：直接使用作品链接，无需秘钥
2. **开发者接入**：需要开通开发者服务，获取开发者播放链接
   - **重要提示：** 开发者秘钥需要在 [开发者工作台](https://9kvr.cn/user/develop/workbench) 获取

## 安全原则

**重要安全提示：**
- 禁止：开发者秘钥不能直接写在前端代码中（会被用户看到）
- 推荐：使用 nginx 代理服务，将秘钥放在服务端
- 最佳实践：通过后端接口获取全景链接，秘钥存储在服务端环境变量中

## React 组件示例

### 方式一：普通链接接入（推荐新手，无需秘钥）

```jsx
import React, {{ useState, useEffect }} from 'react';

function PanoramaViewer({{ workId = '{work_id}' }}) {{
  const [panoramaUrl, setPanoramaUrl] = useState('');

  useEffect(() => {{
    // 普通链接无需秘钥
    setPanoramaUrl(`https://9kvr.cn/tour/index?id=${{workId}}`);
  }}, [workId]);

  return (
    <div style={{ width: '100%', height: '100vh' }}}}>
      <iframe
        src={panoramaUrl}
        frameBorder="0"
        style={{ width: '100%', height: '100%' }}}}
        allowFullScreen
        title="全景作品"
      />
    </div>
  );
}}

export default PanoramaViewer;
```

### 方式二：开发者链接接入（需要秘钥，强烈建议使用 nginx 代理）

**安全警告：** 开发者链接包含秘钥，**必须**通过 nginx 代理或后端接口获取，**禁止**在前端代码中直接使用秘钥！

```jsx
import React, {{ useState, useEffect }} from 'react';

function PanoramaViewer({{ workId = '{work_id}' }}) {{
  const [panoramaUrl, setPanoramaUrl] = useState('');

  useEffect(() => {{
    // 通过接口获取代理后的链接（秘钥在服务端）
    fetch(`/api/panorama/proxy-url?id=${{workId}}`)
      .then(res => res.json())
      .then(data => setPanoramaUrl(data.url))
      .catch(err => console.error('获取全景链接失败:', err));

    // 或者使用 nginx 代理（推荐）
    // setPanoramaUrl(`/panorama/index?id=${{workId}}`);
  }}, [workId]);

  return (
    <div style={{ width: '100%', height: '100vh' }}}}>
      <iframe
        src={panoramaUrl}
        frameBorder="0"
        style={{ width: '100%', height: '100%' }}}}
        allowFullScreen
        title="全景作品"
      />
    </div>
  );
}}

export default PanoramaViewer;
```

#### Nginx 代理配置（服务端，强烈推荐）

在您的 nginx 配置文件中添加：

```nginx
# 方案一：返回代理后的链接（前端通过接口获取）
location /api/panorama/proxy-url {{
  set $secret_key "YOUR_SECRET_KEY";  # 建议从环境变量读取
  set $work_id $arg_id;
  return 200 "https://develop.9kvr.cn/tour/index?key=\\$secret_key&id=\\$work_id";
  add_header Content-Type text/plain;
}}

# 方案二：直接代理整个请求（推荐）
location /panorama/ {{
  proxy_pass https://develop.9kvr.cn/tour/;
  proxy_set_header Host develop.9kvr.cn;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  set $secret_key "YOUR_SECRET_KEY";  # 建议从环境变量读取
  rewrite ^/panorama/(.*)$ /tour/$1?key=$secret_key&$args break;
}}
```

**配置说明：**
- 秘钥存储在 nginx 配置或环境变量中，前端无法获取
- 前端只需访问 `/panorama/index?id=作品ID`，无需知道秘钥
- 建议将秘钥存储在环境变量中，不要硬编码在配置文件中

## 注意事项

1. **安全提示（必须遵守）**
   - 禁止：开发者秘钥不能直接写在前端代码中（会被用户看到）
   - 必须：使用 nginx 代理服务，将秘钥放在服务端
   - 推荐：通过后端接口获取链接，秘钥存储在服务端环境变量中
   - 最佳实践：使用 nginx 直接代理请求，前端无需知道秘钥

2. **iframe 配置**
   - 设置 `allowFullScreen` 属性支持全屏
   - 设置合适的宽高，建议使用 `100vh` 占满视口

## 相关链接

- [获取开发者秘钥](https://9kvr.cn/user/develop/workbench) - 在开发者工作台获取您的秘钥
- [查看详细文档](https://9kvr.cn/user/develop/welcome) - 完整的API接口文档和接入指南

### 更多API接口服务

详细文档中提供了以下API接口服务：

- **getVrList()** - 获取全景作品列表，支持分页查询
- **getVrDetail()** - 获取单个全景作品详细信息
- **openWebview()** - 在小程序webview中打开全景链接
- **createVrPanorama()** - 使用API制作VR全景
- **navigateToMiniProgram()** - 小程序跳转打开全景
- **openEmbeddedMiniProgram()** - 芊云全景打开半屏小程序VR
- **embedIframe()** - 使用iframe嵌入全景播放器

更多详细信息请访问：[开发者文档中心](https://9kvr.cn/user/develop/welcome)"""
        else:
            guide_content = f"""# 原生 JavaScript 接入全景开发指导

## 概述

原生 JavaScript 项目接入全景主要通过 **iframe** 嵌入全景链接来实现。

## 前置条件

1. **普通接入**：直接使用作品链接，无需秘钥
2. **开发者接入**：需要开通开发者服务，获取开发者播放链接
   - **重要提示：** 开发者秘钥需要在 [开发者工作台](https://9kvr.cn/user/develop/workbench) 获取

## 安全原则

**重要安全提示：**
- 禁止：开发者秘钥不能直接写在前端代码中（会被用户看到）
- 推荐：使用 nginx 代理服务，将秘钥放在服务端
- 最佳实践：通过后端接口获取全景链接，秘钥存储在服务端环境变量中

## 原生 JS 示例

### 方式一：普通链接接入（推荐新手，无需秘钥）

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>全景作品</title>
  <style>
    .panorama-container {{
      width: 100%;
      height: 100vh;
    }}
    iframe {{
      width: 100%;
      height: 100%;
      border: none;
    }}
  </style>
</head>
<body>
  <div class="panorama-container">
    <iframe
      id="panoramaFrame"
      src=""
      allowfullscreen
    ></iframe>
  </div>

  <script>
    // 获取作品ID（可以从URL参数获取）
    const urlParams = new URLSearchParams(window.location.search);
    const workId = urlParams.get('id') || '{work_id}';

    // 普通链接无需秘钥
    const panoramaUrl = `https://9kvr.cn/tour/index?id=${{workId}}`;
    document.getElementById('panoramaFrame').src = panoramaUrl;
  </script>
</body>
</html>
```

### 方式二：开发者链接接入（需要秘钥，强烈建议使用 nginx 代理）

**安全警告：** 开发者链接包含秘钥，**必须**通过 nginx 代理或后端接口获取，**禁止**在前端代码中直接使用秘钥！

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>全景作品</title>
  <style>
    .panorama-container {{
      width: 100%;
      height: 100vh;
    }}
    iframe {{
      width: 100%;
      height: 100%;
      border: none;
    }}
  </style>
</head>
<body>
  <div class="panorama-container">
    <iframe
      id="panoramaFrame"
      src=""
      allowfullscreen
    ></iframe>
  </div>

  <script>
    // 获取作品ID（可以从URL参数获取）
    const urlParams = new URLSearchParams(window.location.search);
    const workId = urlParams.get('id') || '{work_id}';

    // 通过接口获取代理后的链接（秘钥在服务端）
    fetch(`/api/panorama/proxy-url?id=${{workId}}`)
      .then(res => res.json())
      .then(data => {{
        document.getElementById('panoramaFrame').src = data.url;
      }})
      .catch(err => {{
        console.error('获取全景链接失败:', err);
      }});

    // 或者使用 nginx 代理（推荐）
    // document.getElementById('panoramaFrame').src = `/panorama/index?id=${{workId}}`;
  </script>
</body>
</html>
```

#### Nginx 代理配置（服务端，强烈推荐）

在您的 nginx 配置文件中添加：

```nginx
# 方案一：返回代理后的链接（前端通过接口获取）
location /api/panorama/proxy-url {{
  set $secret_key "YOUR_SECRET_KEY";  # 建议从环境变量读取
  set $work_id $arg_id;
  return 200 "https://develop.9kvr.cn/tour/index?key=\\$secret_key&id=\\$work_id";
  add_header Content-Type text/plain;
}}

# 方案二：直接代理整个请求（推荐）
location /panorama/ {{
  proxy_pass https://develop.9kvr.cn/tour/;
  proxy_set_header Host develop.9kvr.cn;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  set $secret_key "YOUR_SECRET_KEY";  # 建议从环境变量读取
  rewrite ^/panorama/(.*)$ /tour/$1?key=$secret_key&$args break;
}}
```

**配置说明：**
- 秘钥存储在 nginx 配置或环境变量中，前端无法获取
- 前端只需访问 `/panorama/index?id=作品ID`，无需知道秘钥
- 建议将秘钥存储在环境变量中，不要硬编码在配置文件中

## 注意事项

1. **安全提示（必须遵守）**
   - 禁止：开发者秘钥不能直接写在前端代码中（会被用户看到）
   - 必须：使用 nginx 代理服务，将秘钥放在服务端
   - 推荐：通过后端接口获取链接，秘钥存储在服务端环境变量中
   - 最佳实践：使用 nginx 直接代理请求，前端无需知道秘钥

2. **iframe 配置**
   - 设置 `allowfullscreen` 属性支持全屏
   - 设置合适的宽高，建议使用 `100vh` 占满视口

## 相关链接

- [获取开发者秘钥](https://9kvr.cn/user/develop/workbench) - 在开发者工作台获取您的秘钥
- [查看详细文档](https://9kvr.cn/user/develop/welcome) - 完整的API接口文档和接入指南

### 更多API接口服务

详细文档中提供了以下API接口服务：

- **getVrList()** - 获取全景作品列表，支持分页查询
- **getVrDetail()** - 获取单个全景作品详细信息
- **openWebview()** - 在小程序webview中打开全景链接
- **createVrPanorama()** - 使用API制作VR全景
- **navigateToMiniProgram()** - 小程序跳转打开全景
- **openEmbeddedMiniProgram()** - 芊云全景打开半屏小程序VR
- **embedIframe()** - 使用iframe嵌入全景播放器

更多详细信息请访问：[开发者文档中心](https://9kvr.cn/user/develop/welcome)"""

        return {
            "content": [
                {
                    "type": "text",
                    "text": guide_content,
                },
            ],
        }

    async def getExistingProjectGuide(self, args: Any) -> Dict[str, Any]:
        """获取现有项目接入指导

        Args:
            args: 包含 project_type、tech_stack、work_id 的参数

        Returns:
            Markdown 格式的开发指导文档
        """
        project_type = args.get("project_type", "website") if isinstance(args, dict) else "website"
        tech_stack = args.get("tech_stack", "") if isinstance(args, dict) else ""
        work_id = args.get("work_id", "YOUR_WORK_ID") if isinstance(args, dict) else "YOUR_WORK_ID"

        normal_url = f"https://9kvr.cn/tour/index?id={work_id}"
        developer_url = f"https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id={work_id}"
        if tech_stack:
            tech_stack_section = f"""### {tech_stack} 项目

根据您的技术栈（{tech_stack}），可以参考以下方式：

1. **组件化方式**：将 iframe 封装成组件
2. **路由集成**：在路由中配置全景页面
3. **API 集成**：通过 API 获取作品数据"""
        else:
            tech_stack_section = """### 通用接入方式

1. **静态页面**：直接在 HTML 中添加 iframe
2. **动态页面**：通过 JavaScript 动态创建 iframe
3. **SPA 应用**：在路由组件中嵌入 iframe"""

        if project_type == "website":
            guide_content = f"""# 现有网站接入全景指导

## 概述

将全景功能接入到现有网站中，主要通过 iframe 嵌入的方式实现。

## 前置条件

1. **普通接入**：直接使用作品链接，无需秘钥
2. **开发者接入**：需要开通开发者服务，获取开发者播放链接
   - **重要提示：** 开发者秘钥需要在 [开发者工作台](https://9kvr.cn/user/develop/workbench) 获取

## 安全原则

**重要安全提示：**
- 禁止：开发者秘钥不能直接写在前端代码中（会被用户看到）
- 推荐：使用 nginx 代理服务，将秘钥放在服务端
- 最佳实践：通过后端接口获取全景链接，秘钥存储在服务端环境变量中

## 接入方案

### 方案一：普通链接直接嵌入（推荐新手，无需秘钥）

在需要展示全景的页面中，直接添加 iframe：

```html
<iframe
  src="https://9kvr.cn/tour/index?id={work_id}"
  frameborder="0"
  style="width: 100%; height: 600px;"
  allowfullscreen
></iframe>
```

### 方案二：开发者链接接入（需要秘钥，强烈建议使用 nginx 代理）

**安全警告：** 开发者链接包含秘钥，**必须**通过 nginx 代理或后端接口获取，**禁止**在前端代码中直接使用秘钥！

#### 前端代码（使用 nginx 代理）

```html
<iframe
  src="/panorama/index?id={work_id}"
  frameborder="0"
  style="width: 100%; height: 600px;"
  allowfullscreen
></iframe>
```

#### Nginx 代理配置（服务端，强烈推荐）

在您的 nginx 配置文件中添加：

```nginx
# 直接代理整个请求（推荐）
location /panorama/ {{
  proxy_pass https://develop.9kvr.cn/tour/;
  proxy_set_header Host develop.9kvr.cn;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  set $secret_key "YOUR_SECRET_KEY";  # 建议从环境变量读取
  rewrite ^/panorama/(.*)$ /tour/$1?key=$secret_key&$args break;
}}
```

### 方案三：通过后端 API 动态加载

```javascript
// 通过后端接口获取全景链接（秘钥在服务端）
fetch(`/api/panorama/proxy-url?id={work_id}`)
  .then(res => res.json())
  .then(data => {{
    const iframe = document.createElement('iframe');
    iframe.src = data.url;
    iframe.style.width = '100%';
    iframe.style.height = '600px';
    iframe.setAttribute('allowfullscreen', '');
    document.body.appendChild(iframe);
  }});
```

**错误示例（禁止这样做）：**

```javascript
// 错误：秘钥暴露在前端代码中，用户可以看到
fetch('https://develop.9kvr.cn/api/develop/info.html?key=YOUR_SECRET_KEY')
  .then(res => res.json())
  .then(data => {{
    data.list.forEach(work => {{
      const iframe = document.createElement('iframe');
      // 错误：秘钥直接写在代码中
      iframe.src = `https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id=${{work.work_id}}`;
      document.body.appendChild(iframe);
    }});
  }});
```

## 技术栈适配

{tech_stack_section}

## 相关链接

- [获取开发者秘钥](https://9kvr.cn/user/develop/workbench) - 在开发者工作台获取您的秘钥
- [查看详细文档](https://9kvr.cn/user/develop/welcome) - 完整的API接口文档和接入指南

### 更多API接口服务

详细文档中提供了以下API接口服务：

- **getVrList()** - 获取全景作品列表，支持分页查询
- **getVrDetail()** - 获取单个全景作品详细信息
- **openWebview()** - 在小程序webview中打开全景链接
- **createVrPanorama()** - 使用API制作VR全景
- **navigateToMiniProgram()** - 小程序跳转打开全景
- **openEmbeddedMiniProgram()** - 芊云全景打开半屏小程序VR
- **embedIframe()** - 使用iframe嵌入全景播放器

更多详细信息请访问：[开发者文档中心](https://9kvr.cn/user/develop/welcome)"""
        elif project_type == "app":
            guide_content = f"""# 移动应用接入全景指导

## 概述

移动应用（iOS/Android）接入全景，主要通过 WebView 组件加载全景链接。

## 前置条件

1. **普通接入**：直接使用作品链接，无需秘钥
2. **开发者接入**：需要开通开发者服务，获取开发者播放链接
   - **重要提示：** 开发者秘钥需要在 [开发者工作台](https://9kvr.cn/user/develop/workbench) 获取

## 安全原则

**重要安全提示：**
- **原生应用可以使用秘钥**：iOS/Android 原生应用代码是编译后的，用户无法直接查看，可以在代码中使用秘钥
- **React Native 建议使用后端接口**：React Native 的 JS 代码可能被反编译，建议通过后端接口获取链接
- **网页禁止使用秘钥**：网页代码用户可以直接查看，**禁止**在前端代码中使用秘钥

## 接入方案

### 方式一：普通链接接入（推荐新手，无需秘钥）

#### iOS (Swift)

```swift
import WebKit

class PanoramaViewController: UIViewController {{
  var webView: WKWebView!

  override func viewDidLoad() {{
    super.viewDidLoad()

    let config = WKWebViewConfiguration()
    webView = WKWebView(frame: view.bounds, configuration: config)
    view.addSubview(webView)

    // 普通链接无需秘钥
    let url = URL(string: "https://9kvr.cn/tour/index?id={work_id}")!
    let request = URLRequest(url: url)
    webView.load(request)
  }}
}}
```

#### Android (Kotlin)

```kotlin
import android.webkit.WebView
import android.webkit.WebViewClient

class PanoramaActivity : AppCompatActivity() {{
  private lateinit var webView: WebView

  override fun onCreate(savedInstanceState: Bundle?) {{
    super.onCreate(savedInstanceState)

    webView = WebView(this)
    setContentView(webView)

    webView.settings.javaScriptEnabled = true
    webView.webViewClient = WebViewClient()

    // 普通链接无需秘钥
    val url = "https://9kvr.cn/tour/index?id={work_id}"
    webView.loadUrl(url)
  }}
}}
```

### 方式二：开发者链接接入（需要秘钥）

#### iOS (Swift) - 可以使用秘钥

```swift
import WebKit

class PanoramaViewController: UIViewController {{
  var webView: WKWebView!
  let secretKey = "YOUR_SECRET_KEY"  // 原生应用可以使用秘钥

  override func viewDidLoad() {{
    super.viewDidLoad()

    let config = WKWebViewConfiguration()
    webView = WKWebView(frame: view.bounds, configuration: config)
    view.addSubview(webView)

    let workId = "YOUR_WORK_ID"
    let urlString = "https://develop.9kvr.cn/tour/index?key=\\(secretKey)&id=\\(workId)"
    let url = URL(string: urlString)!
    let request = URLRequest(url: url)
    webView.load(request)
  }}
}}
```

#### Android (Kotlin) - 可以使用秘钥

```kotlin
import android.webkit.WebView
import android.webkit.WebViewClient

class PanoramaActivity : AppCompatActivity() {{
  private lateinit var webView: WebView
  private val secretKey = "YOUR_SECRET_KEY"  // 原生应用可以使用秘钥

  override fun onCreate(savedInstanceState: Bundle?) {{
    super.onCreate(savedInstanceState)

    webView = WebView(this)
    setContentView(webView)

    webView.settings.javaScriptEnabled = true
    webView.webViewClient = WebViewClient()

    val workId = "YOUR_WORK_ID"
    val url = "https://develop.9kvr.cn/tour/index?key=$secretKey&id=$workId"
    webView.loadUrl(url)
  }}
}}
```

#### React Native - 建议使用后端接口

```jsx
import {{ WebView }} from 'react-native-webview';
import {{ useState, useEffect }} from 'react';

function PanoramaScreen({{ workId = '{work_id}' }}) {{
  const [panoramaUrl, setPanoramaUrl] = useState('');

  useEffect(() => {{
    // 推荐：通过后端接口获取链接（秘钥在服务端）
    fetch(`/api/panorama/proxy-url?id=${{workId}}`)
      .then(res => res.json())
      .then(data => setPanoramaUrl(data.url))
      .catch(err => console.error('获取全景链接失败:', err));

    // 或者：如果必须在前端使用，建议将秘钥存储在环境变量中
    // const secretKey = process.env.PANORAMA_SECRET_KEY;
    // setPanoramaUrl(`https://develop.9kvr.cn/tour/index?key=${{secretKey}}&id=${{workId}}`);
  }}, [workId]);

  return (
    <WebView
      source={{{{ uri: panoramaUrl }}
      style={{{{ flex: 1 }}
    />
  );
}}
```

## 相关链接

- [获取开发者秘钥](https://9kvr.cn/user/develop/workbench) - 在开发者工作台获取您的秘钥
- [查看详细文档](https://9kvr.cn/user/develop/welcome) - 完整的API接口文档和接入指南

### 更多API接口服务

详细文档中提供了以下API接口服务：

- **getVrList()** - 获取全景作品列表，支持分页查询
- **getVrDetail()** - 获取单个全景作品详细信息
- **openWebview()** - 在小程序webview中打开全景链接
- **createVrPanorama()** - 使用API制作VR全景
- **navigateToMiniProgram()** - 小程序跳转打开全景
- **openEmbeddedMiniProgram()** - 芊云全景打开半屏小程序VR
- **embedIframe()** - 使用iframe嵌入全景播放器

更多详细信息请访问：[开发者文档中心](https://9kvr.cn/user/develop/welcome)"""
        else:
            guide_content = f"""# CMS 系统接入全景指导

## 概述

在 CMS 系统中接入全景，可以通过自定义字段、插件或模块的方式实现。

## 前置条件

1. **普通接入**：直接使用作品链接，无需秘钥
2. **开发者接入**：需要开通开发者服务，获取开发者播放链接
   - **重要提示：** 开发者秘钥需要在 [开发者工作台](https://9kvr.cn/user/develop/workbench) 获取

## 安全原则

**重要安全提示：**
- 禁止：开发者秘钥不能直接写在前端代码中（会被用户看到）
- 推荐：使用 nginx 代理服务，将秘钥放在服务端
- 最佳实践：通过后端接口获取全景链接，秘钥存储在服务端环境变量中

## 接入方案

### 方案一：普通链接接入（推荐新手，无需秘钥）

#### 1. 添加自定义字段

在内容编辑器中添加"全景作品ID"字段：

```html
<!-- 在文章内容中插入全景 -->
<div class="panorama-embed">
  <iframe
    src="https://9kvr.cn/tour/index?id={{{{work_id}}"
    frameborder="0"
    style="width: 100%; height: 600px;"
    allowfullscreen
  ></iframe>
</div>
```

### 方案二：开发者链接接入（需要秘钥，强烈建议使用 nginx 代理）

**安全警告：** 开发者链接包含秘钥，**必须**通过 nginx 代理或后端接口获取，**禁止**在前端代码中直接使用秘钥！

#### 1. 使用 nginx 代理（推荐）

```html
<!-- 前端代码：使用代理后的链接 -->
<div class="panorama-embed">
  <iframe
    src="/panorama/index?id={{{{work_id}}"
    frameborder="0"
    style="width: 100%; height: 600px;"
    allowfullscreen
  ></iframe>
</div>
```

**Nginx 配置（服务端）：**

```nginx
location /panorama/ {{
  proxy_pass https://develop.9kvr.cn/tour/;
  proxy_set_header Host develop.9kvr.cn;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  set $secret_key "YOUR_SECRET_KEY";  # 建议从环境变量读取
  rewrite ^/panorama/(.*)$ /tour/$1?key=$secret_key&$args break;
}}
```

#### 2. 创建插件/模块（使用后端接口）

```php
// WordPress 插件示例
function panorama_shortcode($atts) {{
  $work_id = $atts['id'] ?? '';

  // 通过后端接口获取链接（秘钥在服务端）
  $secret_key = get_option('panorama_secret_key');  // 从数据库或配置读取
  $url = "https://develop.9kvr.cn/tour/index?key=" . $secret_key . "&id=" . $work_id;

  return '<iframe src="' . esc_url($url) . '"
          style="width:100%;height:600px;" frameborder="0" allowfullscreen></iframe>';
}}
add_shortcode('panorama', 'panorama_shortcode');

// 使用：[panorama id="YOUR_WORK_ID"]
```

#### 3. API 集成（使用后端接口）

```javascript
// 通过后端接口获取作品数据（秘钥在服务端）
async function getPanoramaWorks() {{
  // 前端调用自己的后端接口
  const res = await fetch('/api/panorama/works');
  const data = await res.json();
  return data.list;
}}

// 后端接口示例（Node.js/Express）
app.get('/api/panorama/works', async (req, res) => {{
  const secretKey = process.env.PANORAMA_SECRET_KEY;  // 从环境变量读取
  const response = await fetch(`https://develop.9kvr.cn/api/develop/info.html?key=${{secretKey}}`);
  const data = await response.json();
  res.json(data);
}});
```

**错误示例（禁止这样做）：**

```javascript
// 错误：秘钥暴露在前端代码中，用户可以看到
async function getPanoramaWorks() {{
  const res = await fetch('https://develop.9kvr.cn/api/develop/info.html?key=YOUR_SECRET_KEY');
  const data = await res.json();
  return data.list;
}}
```

## 相关链接

- [获取开发者秘钥](https://9kvr.cn/user/develop/workbench) - 在开发者工作台获取您的秘钥
- [查看详细文档](https://9kvr.cn/user/develop/welcome) - 完整的API接口文档和接入指南

### 更多API接口服务

详细文档中提供了以下API接口服务：

- **getVrList()** - 获取全景作品列表，支持分页查询
- **getVrDetail()** - 获取单个全景作品详细信息
- **openWebview()** - 在小程序webview中打开全景链接
- **createVrPanorama()** - 使用API制作VR全景
- **navigateToMiniProgram()** - 小程序跳转打开全景
- **openEmbeddedMiniProgram()** - 芊云全景打开半屏小程序VR
- **embedIframe()** - 使用iframe嵌入全景播放器

更多详细信息请访问：[开发者文档中心](https://9kvr.cn/user/develop/welcome)"""

        return {
            "content": [
                {
                    "type": "text",
                    "text": guide_content,
                },
            ],
        }

    async def generateIntegrationCode(self, args: Any) -> Dict[str, Any]:
        """生成接入代码

        Args:
            args: 包含 type、platform、framework、work_id、developer_url、use_proxy 的参数

        Returns:
            Markdown 格式的代码示例
        """
        args = args if isinstance(args, dict) else {}
        type_ = args.get("type")
        platform = args.get("platform")
        framework = args.get("framework")
        work_id = args.get("work_id", "YOUR_WORK_ID")
        developer_url = args.get("developer_url", f"https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id={work_id}")
        use_proxy = args.get("use_proxy", False)

        if not type_:
            raise ValueError("type 参数是必需的")

        code = ""

        if type_ == "miniprogram":
            if not platform:
                raise ValueError("小程序类型需要指定 platform 参数（wechat/toutiao/kuaishou）")

            platform_name = "微信" if platform == "wechat" else "抖音" if platform == "toutiao" else "快手"
            platform_code = "wx" if platform == "wechat" else "tt" if platform == "toutiao" else "ks"

            code = f"""// {platform_name}小程序接入代码

// 1. WXML 文件
<view class="panorama-container">
  <web-view src="{{{{panoramaUrl}}"></web-view>
</view>

// 2. JS 文件
Page({{
  data: {{
    panoramaUrl: ''
  }},

  onLoad(options) {{
    const workId = options.id || '{work_id}';
    const secretKey = 'YOUR_SECRET_KEY'; // 请替换为您的秘钥

    this.setData({{
      panoramaUrl: `https://develop.9kvr.cn/tour/index?key=${{secretKey}}&id=${{workId}}`
    }});
  }}
}});

// 3. 注意事项
// - 需要在小程序管理后台配置业务域名：develop.9kvr.cn
// - 建议将秘钥存储在服务端，通过接口获取链接"""

        elif type_ == "web":
            is_vue = framework == "vue" or not framework
            is_react = framework == "react"
            is_vanilla = framework == "vanilla"

            if is_vue:
                code = f"""<template>
  <div class="panorama-container">
    <iframe
      :src="panoramaUrl"
      frameborder="0"
      style="width: 100%; height: 100vh;"
      allowfullscreen
    ></iframe>
  </div>
</template>

<script>
export default {{
  name: 'PanoramaViewer',
  data() {{
    return {{
      panoramaUrl: ''
    }}
  }},
  {"async " if use_proxy else ""}mounted() {{
    const workId = this.$route.params.id || '{work_id}';
    {"// 通过接口获取代理后的链接（秘钥在服务端）" if use_proxy else "// 普通链接"}
    {"const res = await this.$axios.get(`/api/panorama/proxy-url?id=${{workId}}`);\n    this.panoramaUrl = res.data.url;" if use_proxy else f"this.panoramaUrl = `https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id=${{workId}}`;"}
  }}
}}
</script>

<style scoped>
.panorama-container {{
  width: 100%;
  height: 100vh;
}}
</style>"""
            elif is_react:
                code = f"""import React, {{ useState, useEffect }} from 'react';

function PanoramaViewer({{ workId = '{work_id}' }}) {{
  const [panoramaUrl, setPanoramaUrl] = useState('');

  useEffect(() => {{
    ( "// 通过接口获取代理后的链接（秘钥在服务端）" if use_proxy else "// 普通链接" )
    ( "fetch(`/api/panorama/proxy-url?id=${workId}`)\n      .then(res => res.json())\n      .then(data => setPanoramaUrl(data.url));" if use_proxy else "setPanoramaUrl(`https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id=${workId}`);" )
  }}, [workId]);

  return (
    <div style={{{{ width: '100%', height: '100vh' }}}}>
      <iframe
        src={{panoramaUrl}}
        frameBorder="0"
        style={{{{ width: '100%', height: '100%' }}}}
        allowFullScreen
        title="全景作品"
      />
    </div>
  );
}}

export default PanoramaViewer;"""
            else:
                code = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>全景作品</title>
  <style>
    .panorama-container {{
      width: 100%;
      height: 100vh;
    }}
    iframe {{
      width: 100%;
      height: 100%;
      border: none;
    }}
  </style>
</head>
<body>
  <div class="panorama-container">
    <iframe id="panoramaFrame" src="" allowfullscreen></iframe>
  </div>

  <script>
    const urlParams = new URLSearchParams(window.location.search);
    const workId = urlParams.get('id') || '{work_id}';

    ( "// 通过接口获取代理后的链接（秘钥在服务端）" if use_proxy else "// 普通链接" )
    ( "fetch(`/api/panorama/proxy-url?id=${workId}`)\n      .then(res => res.json())\n      .then(data => {{\n        document.getElementById('panoramaFrame').src = data.url;\n      }});" if use_proxy else "const panoramaUrl = `https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id=${workId}`;\n    document.getElementById('panoramaFrame').src = panoramaUrl;" )
  </script>
</body>
</html>"""

            if use_proxy:
                code += f"""\n\n// ========== Nginx 代理配置 ==========
// 在 nginx 配置文件中添加：

location /api/panorama/proxy-url {{
  set $secret_key "YOUR_SECRET_KEY";
  set $work_id $arg_id;
  return 200 "https://develop.9kvr.cn/tour/index?key=\\$secret_key&id=\\$work_id";
  add_header Content-Type text/plain;
}}

// 或者直接代理整个请求：

location /panorama/ {{
  proxy_pass https://develop.9kvr.cn/tour/;
  proxy_set_header Host develop.9kvr.cn;
  set $secret_key "YOUR_SECRET_KEY";
  rewrite ^/panorama/(.*)$ /tour/$1?key=$secret_key&$args break;
}}"""

        else:
            code = f"""// 现有项目接入代码示例

// 1. HTML 中嵌入 iframe
<iframe src="https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id={work_id}"
        frameborder="0"
        style="width: 100%; height: 600px;"
        allowfullscreen>
</iframe>

// 2. JavaScript 动态创建
const iframe = document.createElement('iframe');
iframe.src = `https://develop.9kvr.cn/tour/index?key=YOUR_SECRET_KEY&id=${{workId}}`;
iframe.style.width = '100%';
iframe.style.height = '600px';
iframe.setAttribute('allowfullscreen', '');
document.body.appendChild(iframe);"""

        lang = "javascript" if type_ == "miniprogram" else "vue" if type_ == "web" and framework == "vue" else "jsx" if type_ == "web" and framework == "react" else "html"

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"""# 生成的接入代码

```{lang}
{code}
```

## 使用说明

1. 将代码中的 `YOUR_WORK_ID` 替换为实际的作品ID
2. {"将 `YOUR_SECRET_KEY` 替换为您的开发者秘钥" if type_ == "miniprogram" or use_proxy else "如需使用开发者功能，请配置 nginx 代理隐藏秘钥"}
3. 根据实际需求调整样式和参数""",
                },
            ],
        }
