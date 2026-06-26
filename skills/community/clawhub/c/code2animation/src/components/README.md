# Components

## PlaybackControls.tsx

播放控制栏组件，从主App组件中提取出来以提高代码的可维护性和复用性。

### Props

- **项目和状态**:
  - `projects`: 所有项目的对象
  - `activeProject`: 当前活跃的项目ID
  - `isGenerating`: 是否正在生成音频

- **播放状态**:
  - `isPlaying`: 是否正在播放
  - `currentClipIndex`: 当前片段索引
  - `currentTime`: 当前播放时间
  - `clipDuration`: 片段总时长
  - `totalClips`: 总片段数

- **UI状态**:
  - `isPortrait`: 是否为竖屏模式
  - `disableTransitions`: 是否禁用过渡效果

- **事件处理器**:
  - `onProjectChange`: 项目切换回调
  - `onTogglePlay`: 播放/暂停切换回调
  - `onNextClip`: 下一个片段回调
  - `onPrevClip`: 上一个片段回调
  - `onReset`: 重置回调
  - `onToggleOrientation`: 切换屏幕方向回调
  - `onToggleTransitions`: 切换过渡效果回调

### 功能

1. **项目选择**: 下拉菜单选择不同的视频项目
2. **音频生成状态**: 显示音频生成进度指示器
3. **屏幕方向切换**: 在横屏和竖屏模式间切换
4. **过渡效果控制**: 启用/禁用片段间的过渡动画
5. **播放控制**: 播放、暂停、上一个、下一个片段
6. **进度显示**: 显示当前片段和时间信息
7. **重置功能**: 重置到开始状态

### 样式

使用Tailwind CSS进行样式设计，采用深色主题配色方案，绿色强调色用于活跃状态。