import React from "react";
import { useCurrentFrame } from "remotion";
import { CoverScene } from "./scenes/Cover";
import { Chapter1Scene } from "./scenes/Chapter1";
import { EndScene } from "./scenes/End";

// 帧边界（必须先渲染一次用 ffprobe 确认实际帧数后用这个公式填）：
// F[i] = round(前 i 段累计秒数 / 总秒数 x 实际渲染总帧数)
// 模板值仅为占位，第一遍渲染后必须修正
const F = [0, 360, 1140, 5400];

function prog(t: number, s: number, d: number): number {
  return Math.min(1, Math.max(0, (t - s) / d));
}

export const Scene: React.FC = () => {
  const f = useCurrentFrame();
  if (f < F[1])  return <CoverScene     p={prog(f, F[0], 30)} />;
  if (f < F[2])  return <Chapter1Scene  p={prog(f, F[1], 30)} />;
  return <EndScene p={prog(f, F[2], 30)} />;
};
