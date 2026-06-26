# JS API 安全密钥使用

本章将介绍关于安全密钥的使用，通过代理服务器转发方式来设置。

为了增强安全性，建议将安全密钥存储在服务器端，并通过服务器端生成地图 JS API 的请求 URL。这样可以避免将密钥直接以明文的方式暴露给 Web 端代码中，减少密钥被滥用的风险。

## 获取安全密钥

在使用滴图出行开放平台所提供的 JS API 能力之前，需提前获取 JS API 相关的安全密钥。其安全密钥包含一个**服务端key**，和一个**客户端key**，需要配合使用。

请您登录[【官网控制台】](https://lbs.xiaojukeji.com/console/fe/managekey)，在【创建 key】中自助完成申请。

## 通过代理服务器转发（推荐）

以Nginx反向代理为例，参考以下两个location配置，进行反向代理设置，分别对应 Web 服务以及 Web 静态文件。需要将以下代码配置中的 `客户端key` 替换为你获取到的对应key。

### 前端配置

```html
<script>
  window._DiMapSecurityConfig = {
    serviceHost: "你的代理服务器域名"
    // 例如：serviceHost: 'http://1.1.1.1:80/api/v2/web/'
  }
</script>
```

### Nginx 配置

```nginx
server {
  listen       80;             # nginx端口设置，可按实际端口修改
  server_name  127.0.0.1;      # nginx server_name 对应进行配置，可按实际添加或修改

  # Web服务API 代理
  location /api/v2/web/ {
    set $args "$args&jscode=客户端key";
    proxy_pass https://lbs.xiaojukeji.com/api/v2/web/;
  }

  # Web静态文件 代理
  location /api/v2/static/ {
    set $args "$args&jscode=客户端key";
    proxy_pass https://lbs.xiaojukeji.com/api/v2/static/;
  }
}
```

保存相关配置之后需要通过命令 `nginx -s reload` 重新加载nginx配置文件。

### JS API 使用代码

```html
<div id="container" style="width:100vw; height:100vh"></div>
<script>
  window.DiMapLoader.load({
    key: "您申请的服务端key"
  }).then(({ DiMap }) => {
    new DiMap.Map({
      container: "container",
      style: "dimap://styles/normal"
    })
  })
</script>
```

**提示：** 本例使用Nginx为例，你也可以选择其他方式代理转发，如 Java、Node 服务等。

## 通过明文方式设置（不推荐）

**警告：** JS API 客户端key以明文方式设置，不建议在生产环境使用（不安全）。

**注意：** 密钥设置必须在 JS API 脚本加载之前进行设置，否则设置无效。

### JS API 脚本同步加载示例

```html
<div id="container" style="width:100vw; height:100vh"></div>

<script type="text/javascript">
  window._DiMapSecurityConfig = {
    securityJsCode: "客户端key",
  };
</script>

<script src="https://lbs.xiaojukeji.com/api/v2/static/loader.js"></script>

<script type="text/javascript">
  // 地图初始化应该在地图容器div已经添加到DOM树之后
  window.DiMapLoader.load({
    key: "服务端key"
  }).then(({ DiMap }) => {
    new DiMap.Map({
      container: "container",
      style: "dimap://styles/normal"
    })
  })
</script>
```
