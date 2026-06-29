/**
 * theme.example.ts — a starting Ant Design v5 theme.
 *
 * Demonstrates the recommended pattern: set a few SEED tokens (the system re-derives the rest),
 * pick ALGORITHM(s) for light/dark/compact, and scope a handful of COMPONENT tokens. Consume this
 * with <ConfigProvider theme={getTheme(mode)}>. Never hardcode hex/px in components — read tokens
 * via theme.useToken() so dark/compact themes stay consistent automatically.
 *
 * Usage:
 *   import { ConfigProvider } from 'antd'
 *   import { getTheme } from './theme.example'
 *   <ConfigProvider theme={getTheme('light')}> <App/> </ConfigProvider>
 */
import { theme, type ThemeConfig } from 'antd'

export type ThemeMode = 'light' | 'dark' | 'compact' | 'dark-compact'

/** Seed tokens = your design intent. Change these to rebrand; the algorithm derives palettes,
 *  hover/active states, text opacities, spacing scale, etc. */
const seedToken: ThemeConfig['token'] = {
  // Brand & status (v5 defaults shown — override colorPrimary to rebrand)
  colorPrimary: '#1677FF',
  colorSuccess: '#52C41A',
  colorWarning: '#FAAD14',
  colorError: '#FF4D4F',
  colorInfo: '#1677FF',

  // Shape & type
  borderRadius: 6, // 2 = sharp/enterprise, 8 = friendlier
  fontSize: 14, // base; line-height ~22px is derived

  // Spacing seeds (the 8px rhythm derives from these 4px steps)
  sizeUnit: 4,
  sizeStep: 4,

  // System font stack (no webfont load); ensure CJK fallback in your global CSS
  fontFamily:
    "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, " +
    "'PingFang SC', 'Noto Sans', 'Microsoft YaHei', sans-serif, 'Apple Color Emoji'",
}

/** Component tokens = scoped overrides for ONE component (small blast radius — Tesler's Law).
 *  Prefer these over global hacks when only a component needs to differ. */
const components: ThemeConfig['components'] = {
  Button: {
    controlHeight: 36, // a touch taller for comfortable Fitts's-Law targets
    primaryShadow: 'none', // calmer enterprise look
    fontWeight: 500,
  },
  Table: {
    headerBg: '#F5F7FA',
    headerColor: 'rgba(0,0,0,0.88)',
    rowHoverBg: '#F0F7FF',
    cellPaddingBlock: 12, // density; or use compactAlgorithm globally
  },
  Card: {
    borderRadiusLG: 8,
  },
}

/** Build a ThemeConfig for the given mode. Algorithms are combinable (dark + compact). */
export function getTheme(mode: ThemeMode = 'light'): ThemeConfig {
  const algorithm =
    mode === 'dark'
      ? theme.darkAlgorithm
      : mode === 'compact'
        ? theme.compactAlgorithm
        : mode === 'dark-compact'
          ? [theme.darkAlgorithm, theme.compactAlgorithm]
          : theme.defaultAlgorithm

  return {
    algorithm,
    token: seedToken,
    components,
    // cssVar: true,   // opt into CSS-variable mode (smaller, :root-themeable, better SSR)
    // hashed: true,   // default; set false only if you understand the style-isolation trade-offs
  }
}

/**
 * Example React wiring (for reference):
 *
 *   import { ConfigProvider } from 'antd'
 *   import { useState } from 'react'
 *   import { getTheme, type ThemeMode } from './theme.example'
 *
 *   export default function Root({ children }) {
 *     const [mode, setMode] = useState<ThemeMode>('light')
 *     return (
 *       <ConfigProvider theme={getTheme(mode)}>
 *         {children}
 *       </ConfigProvider>
 *     )
 *   }
 *
 * Reading tokens inside your own components (stay consistent, inherit dark/compact for free):
 *
 *   const { token } = theme.useToken()
 *   <div style={{ padding: token.padding, color: token.colorTextSecondary,
 *                 background: token.colorBgContainer, borderRadius: token.borderRadius }} />
 */
