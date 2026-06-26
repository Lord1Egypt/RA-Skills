import React from "react";
import { Composition, registerRoot } from "remotion";
import { Scene } from "./Scene";

// 第一遍渲染时填估算值（30fps x 音频总秒数），
// 渲染完用 ffprobe 看实际帧数，再回来改成准确值
const DURATION_IN_FRAMES = 5400;  // 180s x 30fps 估算

registerRoot(() => (
  <Composition
    id="MyVideo"
    component={Scene}
    durationInFrames={DURATION_IN_FRAMES}
    fps={30}
    width={1920}
    height={1080}
  />
));
