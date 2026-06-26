# 故障排查

## 安装问题

---

### 问题 1：`npx create-video@latest` 失败

**难度：** 低

**症状：** `npm ERR! network` 或 `ENOENT: no such file or directory`

**解决方案：**
```bash
# 清理 npm 缓存后重试
npm cache clean --force
npx create-video@latest

# 或指定版本
npx create-video@4 my-project

# 检查 Node.js 版本（需要 >= 18）
node --version
```

---

### 问题 2：`npm install` 后 `npx remotion studio` 报错

**难度：** 低

**症状：** `Cannot find module '@remotion/cli'` 或 `command not found: remotion`

**解决方案：**
```bash
# 确认在项目根目录
ls package.json  # 应该存在

# 重新安装依赖
rm -rf node_modules package-lock.json
npm install

# 验证
npx remotion --version
```

---

## 渲染问题

---

### 问题 3：渲染时画面空白或组件不显示

**难度：** 中

**症状：** 输出视频是黑屏或白屏，组件在 Studio 中也不显示

**常见原因：**
- `useCurrentFrame` 返回值超出 `interpolate` 的输入范围（概率 40%）
- 异步数据未用 `delayRender`/`continueRender` 等待（概率 35%）
- CSS 定位问题导致元素在视口外（概率 25%）

**解决方案：**
```typescript
// 调试：打印当前帧
const frame = useCurrentFrame()
console.log('Current frame:', frame)

// 确保 interpolate 范围正确
const opacity = interpolate(
  frame,
  [0, 30],   // 输入范围
  [0, 1],    // 输出范围
  { extrapolateRight: 'clamp' }  // 超出范围时夹断
)

// 异步数据必须用 delayRender
const [handle] = useState(() => delayRender())
useEffect(() => {
  fetchData().then(data => {
    setData(data)
    continueRender(handle)  // 不调用这个，渲染会一直等待
  })
}, [handle])
```

---

### 问题 4：渲染速度过慢

**难度：** 中

**症状：** 本地渲染 1 分钟视频需要超过 10 分钟

**解决方案：**
```bash
# 增加并发（默认 CPU 核心数的一半）
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --concurrency=8

# 降低质量（开发测试用）
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --scale=0.5     # 缩小分辨率
  --crf=28        # 降低画质

# 只渲染部分帧（快速预览）
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --frames=0-60
```

对于 30 秒以上的视频，考虑使用 Lambda 渲染。

---

### 问题 5：字体未正确加载（使用系统字体或 Google Fonts）

**难度：** 中

**症状：** 渲染视频中字体显示为默认字体，与 Studio 预览不一致

**解决方案：**
```typescript
// 使用 @remotion/google-fonts（推荐）
import { loadFont } from '@remotion/google-fonts/Inter'
import { AbsoluteFill } from 'remotion'

const { fontFamily } = loadFont()

export const MyComp: React.FC = () => (
  <AbsoluteFill>
    <p style={{ fontFamily }}>Text with Inter font</p>
  </AbsoluteFill>
)

// 或使用本地字体文件
import { continueRender, delayRender, staticFile } from 'remotion'

const waitForFont = delayRender()
const fontFace = new FontFace('MyFont', `url('${staticFile('font.woff2')}')`)
fontFace.load().then(() => {
  document.fonts.add(fontFace)
  continueRender(waitForFont)
})
```

---

### 问题 6：Lambda 渲染失败

**难度：** 高

**症状：** `Error: Function timed out` 或 `No such file or directory` 部署错误

**常见原因：**
- Lambda 函数超时（默认 120 秒）（概率 40%）
- S3 存储桶权限不足（概率 30%）
- Site URL 配置错误（概率 30%）

**排查步骤：**
```bash
# 检查 Lambda 函数列表
npx remotion lambda functions ls

# 检查 Sites 列表
npx remotion lambda sites ls

# 查看详细错误
npx remotion lambda render my-video MyVideo --log=verbose
```

**解决方案：**
```bash
# 增加 Lambda 超时时间（部署时指定）
npx remotion lambda functions deploy --timeout=300  # 300 秒

# 检查 IAM 权限（需要 S3、Lambda、CloudWatch 权限）
# 参考: https://remotion.dev/docs/lambda/permissions

# 重新部署 site
npx remotion lambda sites create --site-name=my-video --force
```

---

## 许可证问题

---

### 问题 7：商业使用许可证警告

**难度：** 低

**症状：** 控制台显示 `This project is using Remotion without a company license`

**说明：** Remotion 的许可证要求公司（非个人/学生）在商业使用时购买许可证。

**解决方案：**
- 个人项目/学习：可免费使用
- 公司商业使用：前往 [remotion.dev/license](https://remotion.dev/license) 购买许可证
- 获得许可证 Key 后在环境变量中配置

---

## 网络/环境问题

---

### 问题 8：`npx remotion studio` 端口被占用

**难度：** 低

**症状：** `Error: listen EADDRINUSE :::3000`

**解决方案：**
```bash
# 指定其他端口
npx remotion studio --port=3001

# 或找出并终止占用 3000 端口的进程
lsof -i :3000
kill -9 <PID>
```

---

## 通用诊断

```bash
# 检查 Remotion 版本
npx remotion --version

# 渲染单帧进行快速测试
npx remotion still src/index.ts MyVideo out/frame.png --frame=0

# 详细日志模式
npx remotion render src/index.ts MyVideo out/video.mp4 --log=verbose

# 检查 composition 列表
npx remotion compositions src/index.ts
```

**GitHub Issues：** https://github.com/remotion-dev/remotion/issues

**Discord：** https://remotion.dev/discord

**文档：** https://remotion.dev/docs
