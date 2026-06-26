---
name: doubao-image-auto
description: 豆包 AI 创作自动化 - 通过 CDP 浏览器自动化实现无手动交互的图像生成与提取。工作流：1) 连接已打开的豆包页面 2) 导航到 AI 创作页 3) 输入 prompt 并自动生成 4) 提取生成的图片 URL 5) 下载保存到本地。
---

# doubao-image-auto

通过 OpenClaw 浏览器控制（CDP）自动化完成豆包 AI 创作页面生图。

## 工作原理

1. **连接浏览器** - 通过 CDP 连接到已打开的豆包页面（端口 18800）
2. **导航到 AI 创作页** - 打开 `/chat/create-image`
3. **自动输入** - 在文本框输入 prompt
4. **自动点击生成** - 点击生成按钮
5. **提取图片 URL** - 从页面 DOM 中提取图片地址
6. **下载保存** - 下载到指定目录

## 使用方式

### 方式一：通过 OpenClaw 浏览器（推荐）

```javascript
// 1. 打开豆包 AI 创作页
await browser.navigate('https://www.doubao.com/chat/create-image')

// 2. 输入 prompt（在 textbox 中输入）
await browser.act({
  kind: 'type',
  ref: '<textbox ref>',
  text: '生成一只可爱的老虎头像，动漫风格'
})

// 3. 点击生成按钮
await browser.act({
  kind: 'click',
  ref: '<button ref>'
})

// 4. 等待生成完成后，提取图片 URL
const result = await browser.act({
  fn: `() => {
    const imgs = document.querySelectorAll('img[src*="byteimg"], img[src*="imagex"]');
    return Array.from(imgs).slice(0,4).map(i => i.src);
  }`,
  kind: 'evaluate'
})
```

### 方式二：独立 Node 脚本

```javascript
// doubao-auto-gen.js
const CDP = require('chrome-remote-interface');

async function main() {
  const targets = await CDP.List({ port: 18800 });
  const page = targets.find(t => t.type === 'page' && t.url.startsWith('https://www.doubao.com'));
  if (!page) throw new Error('No Doubao page');

  const client = await CDP({ target: page.id, port: 18800 });
  const { Runtime, Input } = client;
  await Runtime.enable();

  // 导航到 AI 创作页
  await Runtime.evaluate({ expression: 'window.location.href = "https://www.doubao.com/chat/create-image"' });
  await new Promise(r => setTimeout(r, 3000));

  // 输入 prompt
  const prompt = '生成一只可爱的老虎头像，动漫风格';
  await Runtime.evaluate({
    expression: `
      (function(){
        const ta = document.querySelector('textarea');
        if(!ta) return JSON.stringify({ok:false});
        ta.value = '${prompt}';
        ta.dispatchEvent(new Event('input', {bubbles:true}));
        return JSON.stringify({ok:true});
      })()
    `,
    returnByValue: true
  });

  // 按回车发送
  await Input.dispatchKeyEvent({ type: 'keyDown', windowsVirtualKeyCode: 13 });
  await Input.dispatchKeyEvent({ type: 'keyUp', windowsVirtualKeyCode: 13 });

  // 等待生成
  await new Promise(r => setTimeout(r, 15000));

  // 提取图片
  const images = await Runtime.evaluate({
    expression: `
      (function(){
        const imgs = [...document.querySelectorAll('img')].filter(img => 
          img.src.includes('byteimg') || img.src.includes('imagex')
        );
        return JSON.stringify(imgs.map(img => img.src));
      })()
    `,
    returnByValue: true
  });

  console.log('Images:', images.result.value);
  await client.close();
}

main().catch(e => console.error(e));
```

### 图片下载

```powershell
# PowerShell 下载图片
$urls = @('图片URL1', '图片URL2')
$outDir = 'C:\path\to\output'
foreach ($url in $urls) {
  $name = [System.IO.Path]::GetFileName([System.Uri]$url.Split('~')[0]) + '.png'
  Invoke-WebRequest -Uri $url -OutFile (Join-Path $outDir $name)
}
```

## 依赖

- **浏览器** - Chrome/Edge 已打开并启用远程调试（端口 18800）
- **CDP 连接** - OpenClaw 浏览器控制已启动，或独立 chrome-remote-interface
- **网络** - 能访问 doubao.com 和 byteimg.com

## 当前状态

✅ **已完全搞定！** - 不需要浏览器，纯 API 调用，自动保存图片

## 已验证的工作流

```powershell
# 直接生成图片并下载
node doubao_media_api.js chat "生成一只可爱的卡通老虎头像，动漫风格" --download --output "./captures"
```

- ✅ Session 保持有效（无需每次登录）
- ✅ 从 SSE 响应中提取图片 URL
- ✅ 自动下载原图到本地
- ✅ 生成的图片发送给你

## Cookie 复用机制

Session 文件位置：`C:\Users\huang\.doubao_chat_session.json`

每次调用 API 时会自动读取这个 Cookie，不需要打开浏览器。

如需手动刷新 Cookie：

```powershell
node doubao_api.js login-if-needed
```