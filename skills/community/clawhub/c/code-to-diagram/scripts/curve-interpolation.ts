/**
 * 曲线插值算法
 * 
 * 支持的曲线类型：
 * - basis: 三次 B 样条曲线（平滑）
 * - monotoneX: X 轴单调三次插值
 * - monotoneY: Y 轴单调三次插值
 * - stepBefore: 阶梯式（先垂直后水平）
 * - stepAfter: 阶梯式（先水平后垂直）
 */

/**
 * 点坐标
 */
export interface Point {
  x: number
  y: number
}

/**
 * 曲线类型
 */
export type CurveType = 'basis' | 'monotoneX' | 'monotoneY' | 'stepBefore' | 'stepAfter'

/**
 * 将点数组转换为 SVG path 数据
 */
export function pointsToCurvePath(points: Point[], curveType: CurveType = 'basis'): string {
  if (points.length < 2) return ''
  
  switch (curveType) {
    case 'basis':
      return basisCurve(points)
    case 'monotoneX':
      return monotoneXCurve(points)
    case 'monotoneY':
      return monotoneYCurve(points)
    case 'stepBefore':
      return stepBeforeCurve(points)
    case 'stepAfter':
      return stepAfterCurve(points)
    default:
      return basisCurve(points)
  }
}

/**
 * 三次 B 样条曲线
 * 生成平滑的曲线通过所有点
 */
function basisCurve(points: Point[]): string {
  const n = points.length
  if (n < 2) return ''
  if (n === 2) {
    return `M${points[0].x},${points[0].y} L${points[1].x},${points[1].y}`
  }
  
  let path = `M${points[0].x},${points[0].y}`
  
  for (let i = 0; i < n - 1; i++) {
    const p0 = points[Math.max(0, i - 1)]
    const p1 = points[i]
    const p2 = points[i + 1]
    const p3 = points[Math.min(n - 1, i + 2)]
    
    const cp1x = p1.x + (p2.x - p0.x) / 6
    const cp1y = p1.y + (p2.y - p0.y) / 6
    const cp2x = p2.x - (p3.x - p1.x) / 6
    const cp2y = p2.y - (p3.y - p1.y) / 6
    
    path += ` C${cp1x},${cp1y} ${cp2x},${cp2y} ${p2.x},${p2.y}`
  }
  
  return path
}

/**
 * X 轴单调三次插值
 * 保证曲线在 X 轴方向单调递增
 */
function monotoneXCurve(points: Point[]): string {
  const n = points.length
  if (n < 2) return ''
  if (n === 2) {
    return `M${points[0].x},${points[0].y} L${points[1].x},${points[1].y}`
  }
  
  // 计算切线
  const tangents: number[] = []
  for (let i = 0; i < n; i++) {
    if (i === 0) {
      tangents.push((points[1].y - points[0].y) / (points[1].x - points[0].x))
    } else if (i === n - 1) {
      tangents.push((points[n - 1].y - points[n - 2].y) / (points[n - 1].x - points[n - 2].x))
    } else {
      const d0 = (points[i].y - points[i - 1].y) / (points[i].x - points[i - 1].x)
      const d1 = (points[i + 1].y - points[i].y) / (points[i + 1].x - points[i].x)
      tangents.push((d0 + d1) / 2)
    }
  }
  
  let path = `M${points[0].x},${points[0].y}`
  
  for (let i = 0; i < n - 1; i++) {
    const dx = points[i + 1].x - points[i].x
    const cp1x = points[i].x + dx / 3
    const cp1y = points[i].y + tangents[i] * dx / 3
    const cp2x = points[i + 1].x - dx / 3
    const cp2y = points[i + 1].y - tangents[i + 1] * dx / 3
    
    path += ` C${cp1x},${cp1y} ${cp2x},${cp2y} ${points[i + 1].x},${points[i + 1].y}`
  }
  
  return path
}

/**
 * Y 轴单调三次插值
 * 保证曲线在 Y 轴方向单调递增
 */
function monotoneYCurve(points: Point[]): string {
  const n = points.length
  if (n < 2) return ''
  if (n === 2) {
    return `M${points[0].x},${points[0].y} L${points[1].x},${points[1].y}`
  }
  
  // 计算切线
  const tangents: number[] = []
  for (let i = 0; i < n; i++) {
    if (i === 0) {
      tangents.push((points[1].x - points[0].x) / (points[1].y - points[0].y))
    } else if (i === n - 1) {
      tangents.push((points[n - 1].x - points[n - 2].x) / (points[n - 1].y - points[n - 2].y))
    } else {
      const d0 = (points[i].x - points[i - 1].x) / (points[i].y - points[i - 1].y)
      const d1 = (points[i + 1].x - points[i].x) / (points[i + 1].y - points[i].y)
      tangents.push((d0 + d1) / 2)
    }
  }
  
  let path = `M${points[0].x},${points[0].y}`
  
  for (let i = 0; i < n - 1; i++) {
    const dy = points[i + 1].y - points[i].y
    const cp1x = points[i].x + tangents[i] * dy / 3
    const cp1y = points[i].y + dy / 3
    const cp2x = points[i + 1].x - tangents[i + 1] * dy / 3
    const cp2y = points[i + 1].y - dy / 3
    
    path += ` C${cp1x},${cp1y} ${cp2x},${cp2y} ${points[i + 1].x},${points[i + 1].y}`
  }
  
  return path
}

/**
 * 阶梯式曲线（先垂直后水平）
 */
function stepBeforeCurve(points: Point[]): string {
  const n = points.length
  if (n < 2) return ''
  if (n === 2) {
    return `M${points[0].x},${points[0].y} L${points[1].x},${points[1].y}`
  }
  
  let path = `M${points[0].x},${points[0].y}`
  
  for (let i = 0; i < n - 1; i++) {
    const midY = (points[i].y + points[i + 1].y) / 2
    path += ` L${points[i].x},${midY} L${points[i + 1].x},${midY}`
  }
  
  path += ` L${points[n - 1].x},${points[n - 1].y}`
  
  return path
}

/**
 * 阶梯式曲线（先水平后垂直）
 */
function stepAfterCurve(points: Point[]): string {
  const n = points.length
  if (n < 2) return ''
  if (n === 2) {
    return `M${points[0].x},${points[0].y} L${points[1].x},${points[1].y}`
  }
  
  let path = `M${points[0].x},${points[0].y}`
  
  for (let i = 0; i < n - 1; i++) {
    const midX = (points[i].x + points[i + 1].x) / 2
    path += ` L${midX},${points[i].y} L${midX},${points[i + 1].y}`
  }
  
  path += ` L${points[n - 1].x},${points[n - 1].y}`
  
  return path
}