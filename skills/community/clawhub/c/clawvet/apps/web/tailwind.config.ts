import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        display: ['"DM Serif Display"', "Georgia", "serif"],
        body: ['"JetBrains Mono"', "monospace"],
        sans: ['"Outfit"', "system-ui", "sans-serif"],
      },
      colors: {
        surface: {
          0: "#06060a",
          1: "#0c0c14",
          2: "#11111c",
          3: "#181826",
          4: "#1f1f30",
        },
        accent: {
          DEFAULT: "#00ffaa",
          dim: "#00cc88",
          muted: "#00996644",
          glow: "#00ffaa22",
        },
        threat: {
          critical: "#ff2d55",
          high: "#ff6b35",
          medium: "#ffb800",
          low: "#5ac8fa",
          safe: "#30d158",
        },
        ink: {
          DEFAULT: "#e8e8f0",
          muted: "#7a7a96",
          faint: "#44445a",
        },
      },
      animation: {
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "sweep": "sweep 3s linear infinite",
        "fade-in": "fadeIn 0.6s ease-out forwards",
        "slide-up": "slideUp 0.5s ease-out forwards",
        "scan-line": "scanLine 4s linear infinite",
      },
      keyframes: {
        sweep: {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scanLine: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100vh)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
