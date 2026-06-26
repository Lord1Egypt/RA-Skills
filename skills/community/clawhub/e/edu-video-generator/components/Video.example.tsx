/**
 * Video.tsx - 视频组件示例（自动同步字幕时长）
 * 
 * 关键点：
 * 1. 从 audio-metadata.json 读取实际配音时长
 * 2. 动态计算每个场景的起始帧
 * 3. 使用 config.js 中的参数，禁止硬编码
 */

import { useVideoConfig, useCurrentFrame } from "remotion";
import { COLORS, fadeIn, popIn } from "./layouts";
import { Circle, Calculator } from "lucide-react";

// ⭐ 从 audio-metadata.json 读取实际时长（不是硬编码！）
const metadata = require('../../scripts/audio-metadata.json');

// 动态计算场景帧
const fps = 30;
let startFrame = 0;
const sceneFrames = metadata.map(m => {
  const start = startFrame;
  const duration = Math.ceil(m.duration * fps);
  startFrame += duration;
  return { id: m.id, start, duration };
});

// ⭐ 从 config.js 读取参数
const CONFIG = require('../../scripts/config.js');

export function Video() {
  const { width, height } = useVideoConfig();
  const frame = useCurrentFrame();

  // 找到当前场景
  let currentScene = null;
  let sceneLocalFrame = 0;
  
  for (const sf of sceneFrames) {
    if (frame >= sf.start && frame < sf.start + sf.duration) {
      currentScene = sf.id;
      sceneLocalFrame = frame - sf.start;
      break;
    }
  }

  // ⭐ 使用 config.js 中的字体大小（不是硬编码！）
  const titleSize = CONFIG.fonts.title;
  const formulaSize = Math.min(width * 0.15, 150);

  const containerStyle = {
    width: "100%",
    height: "100%",
    backgroundColor: COLORS.bg1,
    fontFamily: '"Noto Sans CJK SC", sans-serif',
    color: COLORS.white,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  };

  // 渲染不同场景
  // 注意：画面上只显示标题、图示、公式
  // 旁白由字幕显示，不要在画面上重复！
  switch (currentScene) {
    case "intro":
      return (
        <div style={containerStyle}>
          <div style={{ textAlign: "center" }}>
            <Circle 
              size={Math.min(width, height) * 0.35} 
              color={COLORS.accent2}
              strokeWidth={5}
            />
            <h1 style={{
              fontSize: titleSize,
              marginTop: 50,
              fontWeight: "bold",
              opacity: fadeIn(sceneLocalFrame, 10, CONFIG.animation.fadeIn),
            }}>
              圆的面积
            </h1>
          </div>
        </div>
      );

    case "formula":
      return (
        <div style={containerStyle}>
          <div style={{ textAlign: "center" }}>
            <h2 style={{
              fontSize: titleSize * 0.8,
              marginBottom: 40,
              color: COLORS.gray,
              opacity: fadeIn(sceneLocalFrame, 0, CONFIG.animation.fadeIn),
            }}>
              圆的面积公式
            </h2>
            <div style={{
              fontSize: formulaSize * 1.5,
              fontWeight: "bold",
              color: COLORS.accent3,
              opacity: fadeIn(sceneLocalFrame, 10, CONFIG.animation.fadeIn),
              transform: `scale(${popIn(sceneLocalFrame, 10, 30, CONFIG.animation.spring)})`,
            }}>
              S = πr²
            </div>
          </div>
        </div>
      );

    // ... 其他场景

    default:
      return <div style={containerStyle} />;
  }
}
