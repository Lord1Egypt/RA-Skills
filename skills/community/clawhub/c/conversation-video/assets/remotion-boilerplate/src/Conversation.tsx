import {
  useCurrentFrame,
  interpolate,
  Easing,
  Audio,
  staticFile,
  Sequence,
} from "remotion";
import React from "react";

// ═══════════════════════════════════════════════════════════════
//  TEMPLATE: ConversationVideo
//  Copy this file into your Remotion project and customize.
// ═══════════════════════════════════════════════════════════════

// ─── 1. Define your conversation data ─────────────────────────
// Replace this with your own transcript. `duration` is in FRAMES.
// Use 30fps: 1 second = 30 frames.
interface Line {
  speaker: string;
  text: string;
  duration: number; // frames
}

const conversation: Line[] = [
  { speaker: "NARRATOR",   text: "Customer Discovery Interview", duration: 60 },
  { speaker: "INTERVIEWER",text: "Walk me through the moment you first realized...", duration: 75 },
  { speaker: "CUSTOMER",   text: "I was looking for a marketer agent.", duration: 55 },
  { speaker: "INTERVIEWER",text: "What was not working with your current approach?", duration: 60 },
  { speaker: "CUSTOMER",   text: "Posting on social media myself.", duration: 70 },
];

const GAP = 10; // frames between lines

function getLineStarts(): number[] {
  const starts: number[] = [0];
  for (let i = 0; i < conversation.length - 1; i++) {
    starts.push(starts[i] + conversation[i].duration + GAP);
  }
  return starts;
}

const lineStarts = getLineStarts();
export const totalDuration =
  lineStarts[lineStarts.length - 1] +
  conversation[conversation.length - 1].duration +
  30; // tail padding

// ─── 2. Speaker styling config ────────────────────────────────
// Map speaker names → color, text alignment, x-offset animation.
// Copy/paste lines to add more speakers.
const SpeakerConfig: Record<
  string,
  { color: string; align: "left" | "right" | "center"; xOff: number }
> = {
  NARRATOR:    { color: "#cbd5e1", align: "center", xOff: 0 },
  INTERVIEWER: { color: "#60a5fa", align: "left",   xOff: -20 },
  CUSTOMER:    { color: "#34d399", align: "right",  xOff: 20 },
};

// ─── 3. Animated bubble component ─────────────────────────────
const Bubble: React.FC<{ line: Line; start: number }> = ({
  line,
  start,
}) => {
  const frame = useCurrentFrame();
  const cfg = SpeakerConfig[line.speaker] || SpeakerConfig.NARRATOR;

  const enter = interpolate(frame, [start, start + 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  const exit = interpolate(
    frame,
    [start + line.duration - 12, start + line.duration],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  if (frame < start || frame >= start + line.duration) return null;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems:
          cfg.align === "left"
            ? "flex-start"
            : cfg.align === "right"
            ? "flex-end"
            : "center",
        padding: "0 80px",
        opacity: enter * exit,
        transform: `translateX(${interpolate(enter, [0, 1], [cfg.xOff, 0])}px)`,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          maxWidth: "760px",
          padding: "22px 30px",
          borderRadius: "14px",
          background: "rgba(15, 23, 42, 0.9)",
          border: `1.5px solid ${cfg.color}30`,
          boxShadow: `0 8px 28px ${cfg.color}12`,
        }}
      >
        <div
          style={{
            fontSize: "11px",
            fontWeight: 700,
            letterSpacing: "1.2px",
            color: cfg.color,
            marginBottom: "8px",
            textTransform: "uppercase",
          }}
        >
          {line.speaker}
        </div>
        <div
          style={{
            fontSize: "26px",
            lineHeight: 1.4,
            color: "#f8fafc",
            fontWeight: 500,
          }}
        >
          {line.text}
        </div>
      </div>
    </div>
  );
};

// ─── 4. Animated background ───────────────────────────────────
const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = frame * 0.2;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        background:
          "linear-gradient(145deg, #0b1021 0%, #131a3a 50%, #0b1021 100%)",
        overflow: "hidden",
      }}
    >
      {/* Drifting grid */}
      <div
        style={{
          position: "absolute",
          inset: -60,
          backgroundImage: `
            linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px)
          `,
          backgroundSize: "50px 50px",
          transform: `translate(${drift % 50}px, ${(drift * 0.5) % 50}px)`,
        }}
      />
      {/* Floating orbs */}
      <div
        style={{
          position: "absolute",
          top: "20%",
          left: "15%",
          width: "300px",
          height: "300px",
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%)",
          transform: `translate(${Math.sin(frame / 90) * 20}px, ${
            Math.cos(frame / 90) * 20
          }px)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: "15%",
          right: "15%",
          width: "250px",
          height: "250px",
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(52,211,153,0.08) 0%, transparent 70%)",
          transform: `translate(${Math.cos(frame / 110) * 15}px, ${
            Math.sin(frame / 110) * 15
          }px)`,
        }}
      />
    </div>
  );
};

// ─── 5. Optional header bar ───────────────────────────────────
const Header: React.FC = () => {
  const frame = useCurrentFrame();
  const op = interpolate(
    frame,
    [0, 20, totalDuration - 30, totalDuration],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        position: "absolute",
        top: 28,
        left: "50%",
        transform: "translateX(-50%)",
        opacity: op,
        display: "flex",
        alignItems: "center",
        gap: 10,
        zIndex: 10,
      }}
    >
      <div
        style={{
          width: 8,
          height: 8,
          borderRadius: "50%",
          background: "#34d399",
          boxShadow: "0 0 10px #34d39950",
        }}
      />
      <span
        style={{
          fontSize: 13,
          fontWeight: 600,
          color: "#94a3b8",
          letterSpacing: 2,
          textTransform: "uppercase",
        }}
      >
        Live Conversation
      </span>
    </div>
  );
};

// ─── 6. Main video component ──────────────────────────────────
export const ConversationVideo: React.FC = () => {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      {/* Uncomment to add audio: */}
      {/* <Audio src={staticFile("audio.wav")} /> */}

      <Background />
      <Header />
      {conversation.map((line, i) => (
        <Bubble key={i} line={line} start={lineStarts[i]} />
      ))}
    </div>
  );
};
