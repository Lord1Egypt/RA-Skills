/**
 * SVG 后处理模块
 * 
 * 功能：
 * 1. 解析 Mermaid 源码中的曲线配置
 * 2. 将 SVG 中的 polyline 转换为曲线 path
 */

import { pointsToCurvePath, CurveType, Point } from './curve-interpolation.ts'

/**
 * 从 Mermaid 源码中解析曲线配置
 */
export function parseCurveConfig(mmdContent: string): CurveType | null {
  // 匹配 %%{ init: { 'flowchart': { 'curve': 'basis' } } }%%
  const match = mmdContent.match(/%%\s*\{\s*init\s*:\s*\{\s*'flowchart'\s*:\s*\{\s*'curve'\s*:\s*'([^']+)'\s*\}\s*\}\s*\}\s*%%/)
  
  if (match) {
    const curveType = match[1] as CurveType
    const validTypes: CurveType[] = ['basis', 'monotoneX', 'monotoneY', 'stepBefore', 'stepAfter']
    if (validTypes.includes(curveType)) {
      return curveType
    }
  }
  
  return null
}

/**
 * 从 SVG polyline 的 points 属性中提取点坐标
 */
function parsePoints(pointsStr: string): Point[] {
  const points: Point[] = []
  const pairs = pointsStr.trim().split(/\s+/)
  
  for (const pair of pairs) {
    const [x, y] = pair.split(',').map(Number)
    if (!isNaN(x) && !isNaN(y)) {
      points.push({ x, y })
    }
  }
  
  return points
}

/**
 * 将 SVG 中的 polyline 转换为曲线 path
 */
export function convertPolylinesToCurves(svgString: string, curveType: CurveType): string {
  // 匹配所有 polyline 元素
  const polylineRegex = /<polyline([^>]*)points="([^"]*)"([^>]*)\/>/g
  
  return svgString.replace(polylineRegex, (match, before, pointsStr, after) => {
    const points = parsePoints(pointsStr)
    
    if (points.length < 2) {
      return match
    }
    
    const pathData = pointsToCurvePath(points, curveType)
    
    // 保留原始属性，但将 polyline 改为 path，points 改为 d
    const attrs = (before + after).trim()
    
    return `<path ${attrs} d="${pathData}" />`
  })
}

/**
 * 完整的 SVG 曲线转换流程
 */
export function applyCurveToSvg(svgString: string, mmdContent: string): string {
  const curveType = parseCurveConfig(mmdContent)
  
  if (!curveType) {
    return svgString
  }
  
  return convertPolylinesToCurves(svgString, curveType)
}