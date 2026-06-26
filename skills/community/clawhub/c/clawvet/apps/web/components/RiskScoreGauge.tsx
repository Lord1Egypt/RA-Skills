"use client";

function getColor(score: number): string {
  if (score <= 10) return "#30d158";
  if (score <= 25) return "#84cc16";
  if (score <= 50) return "#ffb800";
  if (score <= 75) return "#ff6b35";
  return "#ff2d55";
}

function getGrade(score: number): string {
  if (score <= 10) return "A";
  if (score <= 25) return "B";
  if (score <= 50) return "C";
  if (score <= 75) return "D";
  return "F";
}

export function RiskScoreGauge({
  score,
  size = "lg",
}: {
  score: number;
  size?: "sm" | "lg";
}) {
  const color = getColor(score);
  const grade = getGrade(score);
  const isLg = size === "lg";
  const dim = isLg ? 180 : 80;
  const radius = isLg ? 70 : 30;
  const strokeWidth = isLg ? 8 : 5;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={dim} height={dim} viewBox={`0 0 ${dim} ${dim}`}>
        {/* Background ring */}
        <circle
          cx={dim / 2}
          cy={dim / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-surface-3"
        />
        {/* Glow filter */}
        <defs>
          <filter id={`glow-${score}`}>
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        {/* Progress arc */}
        <circle
          cx={dim / 2}
          cy={dim / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          strokeLinecap="round"
          transform={`rotate(-90 ${dim / 2} ${dim / 2})`}
          filter={`url(#glow-${score})`}
          style={{
            transition: "stroke-dashoffset 1s cubic-bezier(0.34, 1.56, 0.64, 1)",
          }}
        />
      </svg>
      <div className="absolute text-center">
        <div
          className={`font-display ${isLg ? "text-4xl" : "text-lg"} font-bold`}
          style={{ color }}
        >
          {grade}
        </div>
        {isLg && (
          <div className="font-body text-xs text-ink-faint mt-0.5">
            {score}/100
          </div>
        )}
      </div>
    </div>
  );
}
