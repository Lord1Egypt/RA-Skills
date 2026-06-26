# 代码重构总结

## 抽取的文件和功能

### 1. `utils/playbackEngine.ts`
- `processProject()` - 处理项目数据，基于真实语音 word boundaries
- `getCurrentMedia()` - 获取当前应显示的媒体
- `seekToTime()` - 跳转到指定时间
- `getTotalDuration()` - 获取总时长

### 2. `utils/audioManager.ts`
- `generateAudio()` - 调用API生成音频
- `loadAudioFiles()` - 加载音频文件到缓存
- `checkAudioExists()` - 检查音频文件是否存在
- `getSpeechClips()` - 获取包含语音的片段
- 统一管理音频相关操作

### 3. `components/MediaRenderer.tsx`
- `MediaRenderer` - 渲染单个媒体组件
- 处理HTML iframe和占位符显示
- 从App.tsx中抽取的组件

### 4. `components/Player.tsx`
- `Player` - 主播放器组件
- 渲染背景和媒体层
- 使用MediaRenderer渲染具体媒体

### 5. `hooks/useProject.ts`
- 管理项目加载状态
- 处理项目数据获取和缓存
- 提供当前项目信息

### 6. `hooks/usePlayback.ts`
- 管理播放状态（播放/暂停、当前时间、片段索引）
- 处理动画循环和时间更新
- 提供播放控制函数（下一个、上一个、重置）

## 重构效果

### 简化后的架构
- 移除了复杂的过渡动画系统
- 删除了 clipProcessing 和 renderState 模块
- 基于真实语音 word boundaries 的简单时间轴

### 优势
1. **简单性** - 去除了不必要的复杂性，专注核心功能
2. **准确性** - 使用真实的语音时间数据而非估算
3. **可维护性** - 代码结构清晰，易于理解和修改
4. **性能** - 减少了复杂的计算和状态管理

## 使用方式

简化后的播放引擎专注于：
- 按时间显示 iframe 内容
- 同步播放语音
- 基本的播放控制