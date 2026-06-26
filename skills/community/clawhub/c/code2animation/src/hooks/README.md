# Hooks

## useTTS.ts

用于处理文本转语音(TTS)音频播放的React Hook。

### 功能特性

1. **多种音频源支持**:
   - 优先使用预生成的静态音频文件 (`/audio/{projectId}/{clipIndex}.mp3`)
   - 如果静态文件不存在，回退到实时TTS API生成
   - 支持音频元数据加载用于词边界跟踪

2. **词边界跟踪**:
   - 解析TTS元数据JSON文件
   - 实时跟踪当前播放的单词
   - 支持onWordBoundary回调

3. **音频生命周期管理**:
   - 自动资源清理
   - 防止内存泄漏
   - 组件卸载时自动停止音频

4. **播放控制**:
   - `speak()`: 从头开始播放
   - `pause()`: 暂停播放
   - `resume()`: 恢复播放
   - `stop()`: 停止并重置到开始位置

### 使用方法

```typescript
const {
  isSpeaking,
  isLoading,
  duration,
  speak,
  pause,
  resume,
  stop
} = useTTS({
  clip: currentClip,
  projectId: 'agentSaasPromoVideo',
  clipIndex: 0,
  onWordBoundary: (word) => console.log('Current word:', word),
  onEnd: () => console.log('Audio finished')
});
```

### Props

- `clip`: 当前视频片段对象
- `projectId`: 项目ID
- `clipIndex`: 片段索引（用于定位音频文件）
- `onWordBoundary`: 词边界回调函数
- `onEnd`: 音频结束回调函数

### 返回值

- `isSpeaking`: 是否正在播放
- `isLoading`: 是否正在加载音频
- `duration`: 音频时长
- `alignment`: 词边界对齐数据
- `speak/pause/resume/stop`: 播放控制函数

### 音频文件结构

```
public/audio/{projectId}/
├── 0.mp3          # 第一个语音片段
├── 0.json         # 对应的元数据
├── 1.mp3          # 第二个语音片段
├── 1.json         # 对应的元数据
└── ...
```

### 集成说明

Hook已集成到主App组件中，会自动：
- 在片段切换时加载对应音频
- 与视频播放状态同步
- 在项目切换时清理资源
- 处理加载状态显示