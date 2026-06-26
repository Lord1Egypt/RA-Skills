/**
 * 视频排版组件库 v2
 * 
 * 扩展版本，支持更多教育视频场景
 */

import React from 'react';
import { spring, interpolate } from 'remotion';

// ===== 颜色系统 =====
export const COLORS = {
  // 背景
  bg1: '#0f0f23',
  bg2: '#1a1a3e',
  bg3: '#2d2d5a',
  
  // 强调色
  accent1: '#ff6b6b',  // 红
  accent2: '#4ecdc4',  // 青
  accent3: '#ffe66d',  // 黄
  accent4: '#95e1d3',  // 浅青
  accent5: '#a78bfa',  // 紫
  accent6: '#f97316',  // 橙
  accent7: '#ec4899',  // 粉
  
  // 语义色
  success: '#22c55e',
  warning: '#eab308',
  danger: '#ef4444',
  info: '#3b82f6',
  
  // 文字
  white: '#ffffff',
  gray: '#94a3b8',
  darkGray: '#64748b',
  lightGray: '#cbd5e1',
};

// ===== 动画工具 =====

export const fadeIn = (frame, startFrame, duration = 15) => 
  interpolate(frame, [startFrame, startFrame + duration], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp'
  });

export const slideUp = (frame, startFrame, duration = 15, distance = 20) =>
  interpolate(frame, [startFrame, startFrame + duration], [distance, 0], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp'
  });

export const slideIn = (frame, startFrame, duration = 15, direction = 'left', distance = 50) => {
  const axis = direction === 'left' ? -distance : direction === 'right' ? distance : 0;
  const y = direction === 'up' ? distance : direction === 'down' ? -distance : 0;
  return { x: interpolate(frame, [startFrame, startFrame + duration], [axis, 0], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' }), y };
};

export const popIn = (frame, startFrame, fps = 30) =>
  spring({ fps, frame: Math.max(0, frame - startFrame), config: { damping: 12, stiffness: 100 } });

export const scaleIn = (frame, startFrame, duration = 15) =>
  interpolate(frame, [startFrame, startFrame + duration], [0.8, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp'
  });

export const rotateIn = (frame, startFrame, duration = 20) =>
  interpolate(frame, [startFrame, startFrame + duration], [-10, 0], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp'
  });

export const stagger = (index, baseDelay = 8) => baseDelay * index;

// ===== 基础布局 =====

/**
 * Centered - 居中布局
 */
export function Centered({ 
  children, 
  frame, 
  title, 
  subtitle, 
  text,
  icon,
  background = 'gradient1',
  maxWidth = 0.75,
  textAlign = 'center'
}) {
  const bgStyles = {
    gradient1: `linear-gradient(135deg, ${COLORS.bg2}, ${COLORS.bg1})`,
    gradient2: `linear-gradient(180deg, ${COLORS.bg2}, ${COLORS.bg1})`,
    radial: `radial-gradient(ellipse at center, ${COLORS.bg2}, ${COLORS.bg1})`,
    solid: COLORS.bg1,
  };
  
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: bgStyles[background] || bgStyles.gradient1,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '5%',
    }}>
      <div style={{ textAlign, maxWidth: `${maxWidth * 100}%`, width: '100%' }}>
        {icon && (
          <div style={{ 
            marginBottom: 25, 
            opacity: fadeIn(frame, 0, 15),
            display: 'flex',
            justifyContent: textAlign === 'center' ? 'center' : 'flex-start'
          }}>
            {typeof icon === 'function' ? icon(frame) : icon}
          </div>
        )}
        {title && (
          <h1 style={{
            fontSize: 'clamp(32px, 5vw, 56px)',
            color: COLORS.white,
            fontFamily: '"Noto Serif CJK SC", serif',
            fontWeight: 'bold',
            marginBottom: 25,
            lineHeight: 1.4,
            opacity: fadeIn(frame, 0, 15),
          }}>
            {title}
          </h1>
        )}
        {subtitle && (
          <h2 style={{
            fontSize: 'clamp(20px, 3vw, 32px)',
            color: COLORS.accent2,
            fontFamily: '"Noto Serif CJK SC", serif',
            marginBottom: 35,
            opacity: fadeIn(frame, 20, 15),
          }}>
            {subtitle}
          </h2>
        )}
        {text && (
          <p style={{
            fontSize: 'clamp(16px, 2.5vw, 24px)',
            color: COLORS.gray,
            fontFamily: '"Noto Serif CJK SC", serif',
            lineHeight: 2.2,
            opacity: fadeIn(frame, 40, 15),
          }}>
            {text}
          </p>
        )}
        {children}
      </div>
    </div>
  );
}

/**
 * SplitH - 左右分屏
 */
export function SplitH({
  frame,
  leftContent,
  rightContent,
  leftWidth = 0.55,
  rightWidth = 0.45,
  leftBg = 'transparent',
  rightBg = 'transparent',
  gap = 0,
  reverse = false,
  padding = 50,
}) {
  const left = (
    <div style={{
      width: `${leftWidth * 100}%`,
      background: leftBg,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      padding: `${padding}px`,
    }}>
      {typeof leftContent === 'function' ? leftContent(frame) : leftContent}
    </div>
  );
  
  const right = (
    <div style={{
      width: `${rightWidth * 100}%`,
      background: rightBg,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: `${padding}px`,
    }}>
      {typeof rightContent === 'function' ? rightContent(frame) : rightContent}
    </div>
  );
  
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(135deg, ${COLORS.bg2}, ${COLORS.bg1})`,
      display: 'flex',
      flexDirection: 'row',
      gap: `${gap * 100}%`,
    }}>
      {reverse ? right : left}
      {reverse ? left : right}
    </div>
  );
}

/**
 * SplitV - 上下分屏
 */
export function SplitV({
  frame,
  topContent,
  bottomContent,
  topHeight = 0.55,
  bottomHeight = 0.45,
  padding = 30,
}) {
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(180deg, ${COLORS.bg2}, ${COLORS.bg1})`,
      display: 'flex',
      flexDirection: 'column',
    }}>
      <div style={{
        height: `${topHeight * 100}%`,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: `${padding}px`,
      }}>
        {typeof topContent === 'function' ? topContent(frame) : topContent}
      </div>
      <div style={{
        height: `${bottomHeight * 100}%`,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'flex-start',
        padding: `${padding}px`,
      }}>
        {typeof bottomContent === 'function' ? bottomContent(frame) : bottomContent}
      </div>
    </div>
  );
}

/**
 * Diagram - 图解布局
 */
export function Diagram({
  frame,
  title,
  diagram,
  labels = [],
  caption,
  captionAlign = 'center',
}) {
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(180deg, ${COLORS.bg2}, ${COLORS.bg1})`,
      display: 'flex',
      flexDirection: 'column',
    }}>
      {title && (
        <div style={{
          padding: '35px 50px 20px',
          textAlign: 'center',
          opacity: fadeIn(frame, 0, 15),
        }}>
          <h1 style={{
            fontSize: 'clamp(24px, 4vw, 40px)',
            color: COLORS.white,
            fontFamily: '"Noto Serif CJK SC", serif',
            margin: 0,
          }}>
            {title}
          </h1>
        </div>
      )}
      
      <div style={{
        flex: 1,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        position: 'relative',
      }}>
        {typeof diagram === 'function' ? diagram(frame) : diagram}
        
        {labels.map((label, i) => (
          <div key={i} style={{
            position: 'absolute',
            ...label.position,
            opacity: fadeIn(frame, 30 + i * 12, 12),
          }}>
            {label.content}
          </div>
        ))}
      </div>
      
      {caption && (
        <div style={{
          padding: '25px 50px 40px',
          textAlign: captionAlign,
          opacity: fadeIn(frame, 50, 15),
        }}>
          {typeof caption === 'function' ? caption(frame) : caption}
        </div>
      )}
    </div>
  );
}

/**
 * Comparison - 对比布局
 */
export function Comparison({
  frame,
  title,
  items = [],
  summary,
  direction = 'horizontal',
  cardWidth = 280,
}) {
  const isHorizontal = direction === 'horizontal';
  
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(180deg, ${COLORS.bg1}, ${COLORS.bg2})`,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '5%',
    }}>
      {title && (
        <h1 style={{
          fontSize: 'clamp(24px, 4vw, 40px)',
          color: COLORS.white,
          fontFamily: '"Noto Serif CJK SC", serif',
          marginBottom: 40,
          opacity: fadeIn(frame, 0, 15),
        }}>
          {title}
        </h1>
      )}
      
      <div style={{
        display: 'flex',
        flexDirection: isHorizontal ? 'row' : 'column',
        gap: isHorizontal ? 35 : 20,
        marginBottom: 40,
      }}>
        {items.map((item, i) => (
          <div key={i} style={{
            width: isHorizontal ? cardWidth : '100%',
            background: `${item.color}22`,
            borderRadius: 16,
            padding: 25,
            opacity: fadeIn(frame, 15 + i * 10, 15),
            borderLeft: `4px solid ${item.color}`,
          }}>
            {item.icon && <div style={{ marginBottom: 15 }}>{item.icon}</div>}
            <h3 style={{
              fontSize: 'clamp(18px, 2.5vw, 26px)',
              color: item.color,
              fontFamily: '"Noto Serif CJK SC", serif',
              marginBottom: 15,
            }}>
              {item.title}
            </h3>
            <p style={{
              fontSize: 'clamp(14px, 2vw, 18px)',
              color: COLORS.white,
              fontFamily: '"Noto Serif CJK SC", serif',
              lineHeight: 1.8,
              margin: 0,
              whiteSpace: 'pre-line',
            }}>
              {item.content}
            </p>
          </div>
        ))}
      </div>
      
      {summary && (
        <p style={{
          fontSize: 'clamp(16px, 2.2vw, 22px)',
          color: COLORS.accent3,
          fontFamily: '"Noto Serif CJK SC", serif',
          opacity: fadeIn(frame, 40, 15),
          textAlign: 'center',
        }}>
          {summary}
        </p>
      )}
    </div>
  );
}

/**
 * List - 列表布局
 */
export function List({
  frame,
  title,
  items = [],
  numbered = false,
  columns = 1,
  itemDelay = 18,
}) {
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(135deg, ${COLORS.bg2}, ${COLORS.bg1})`,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '5%',
    }}>
      {title && (
        <h1 style={{
          fontSize: 'clamp(28px, 4.5vw, 48px)',
          color: COLORS.white,
          fontFamily: '"Noto Serif CJK SC", serif',
          marginBottom: 50,
          opacity: fadeIn(frame, 0, 15),
        }}>
          {title}
        </h1>
      )}
      
      <div style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gap: 20,
        maxWidth: columns > 1 ? '90%' : '75%',
      }}>
        {items.map((item, i) => {
          const text = typeof item === 'string' ? item : item.text;
          const icon = typeof item === 'object' ? item.icon : null;
          const color = typeof item === 'object' ? item.color : COLORS.accent2;
          
          return (
            <div key={i} style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: 15,
              opacity: fadeIn(frame, itemDelay + i * itemDelay, 15),
              transform: `translateY(${slideUp(frame, itemDelay + i * itemDelay, 15, 15)}px)`,
            }}>
              {numbered ? (
                <div style={{
                  minWidth: 32,
                  height: 32,
                  borderRadius: '50%',
                  background: color,
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  fontSize: 16,
                  fontWeight: 'bold',
                  color: COLORS.bg1,
                }}>
                  {i + 1}
                </div>
              ) : icon ? (
                <div style={{ minWidth: 24 }}>{icon}</div>
              ) : (
                <div style={{
                  minWidth: 8,
                  height: 8,
                  borderRadius: '50%',
                  background: color,
                  marginTop: 10,
                }} />
              )}
              <p style={{
                fontSize: 'clamp(16px, 2.5vw, 24px)',
                color: COLORS.white,
                fontFamily: '"Noto Serif CJK SC", serif',
                lineHeight: 2.2,
                margin: 0,
              }}>
                {text}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ===== 扩展布局 =====

/**
 * Timeline - 时间线布局
 * 用于：步骤、流程、历史
 */
export function Timeline({
  frame,
  title,
  steps = [],
  orientation = 'horizontal', // 'horizontal' | 'vertical'
  color = COLORS.accent2,
}) {
  const isHorizontal = orientation === 'horizontal';
  
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(135deg, ${COLORS.bg2}, ${COLORS.bg1})`,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '5%',
    }}>
      {title && (
        <h1 style={{
          fontSize: 'clamp(28px, 4.5vw, 48px)',
          color: COLORS.white,
          fontFamily: '"Noto Serif CJK SC", serif',
          marginBottom: 50,
          opacity: fadeIn(frame, 0, 15),
        }}>
          {title}
        </h1>
      )}
      
      <div style={{
        display: 'flex',
        flexDirection: isHorizontal ? 'row' : 'column',
        alignItems: isHorizontal ? 'center' : 'flex-start',
        gap: 0,
        position: 'relative',
      }}>
        {/* 连接线 */}
        <div style={{
          position: 'absolute',
          [isHorizontal ? 'top' : 'left']: 20,
          [isHorizontal ? 'left' : 'top']: 0,
          [isHorizontal ? 'right' : 'bottom']: 0,
          [isHorizontal ? 'height' : 'width']: 3,
          [isHorizontal ? 'width' : 'height']: '100%',
          background: `${color}44`,
        }} />
        
        {steps.map((step, i) => (
          <div key={i} style={{
            display: 'flex',
            flexDirection: isHorizontal ? 'column' : 'row',
            alignItems: 'center',
            gap: 20,
            [isHorizontal ? 'flex' : 'marginBottom']: i < steps.length - 1 ? (isHorizontal ? 1 : 50) : 0,
            [isHorizontal ? 'marginLeft' : 'marginLeft']: i > 0 ? (isHorizontal ? 60 : 0) : 0,
            opacity: fadeIn(frame, 20 + i * 15, 15),
            transform: `translate${isHorizontal ? 'X' : 'Y'}(${slideUp(frame, 20 + i * 15, 15, isHorizontal ? 30 : 20)}px)`,
          }}>
            {/* 圆点 */}
            <div style={{
              width: 40,
              height: 40,
              borderRadius: '50%',
              background: color,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              fontSize: 18,
              fontWeight: 'bold',
              color: COLORS.bg1,
              zIndex: 1,
              boxShadow: `0 0 20px ${color}66`,
            }}>
              {i + 1}
            </div>
            
            {/* 内容 */}
            <div style={{ textAlign: isHorizontal ? 'center' : 'left', maxWidth: 200 }}>
              <h3 style={{
                fontSize: 'clamp(16px, 2.2vw, 22px)',
                color: COLORS.white,
                fontFamily: '"Noto Serif CJK SC", serif',
                marginBottom: 8,
              }}>
                {step.title}
              </h3>
              {step.subtitle && (
                <p style={{
                  fontSize: 'clamp(12px, 1.8vw, 16px)',
                  color: COLORS.gray,
                  fontFamily: '"Noto Serif CJK SC", serif',
                  margin: 0,
                }}>
                  {step.subtitle}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/**
 * Quote - 引用布局
 * 用于：强调、名言、重点
 */
export function Quote({
  frame,
  quote,
  author,
  source,
  background = 'gradient1',
  accentColor = COLORS.accent3,
}) {
  return (
    <Centered frame={frame} background={background} maxWidth={0.7}>
      <div style={{
        position: 'relative',
        padding: '40px 60px',
      }}>
        {/* 引号 */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          fontSize: 120,
          color: `${accentColor}33`,
          fontFamily: 'Georgia, serif',
          lineHeight: 1,
        }}>
          "
        </div>
        
        <p style={{
          fontSize: 'clamp(22px, 3.5vw, 36px)',
          color: COLORS.white,
          fontFamily: '"Noto Serif CJK SC", serif',
          lineHeight: 1.8,
          fontStyle: 'italic',
          marginBottom: 30,
          opacity: fadeIn(frame, 15, 20),
          position: 'relative',
          zIndex: 1,
        }}>
          {quote}
        </p>
        
        {author && (
          <p style={{
            fontSize: 'clamp(16px, 2.2vw, 22px)',
            color: accentColor,
            fontFamily: '"Noto Serif CJK SC", serif',
            opacity: fadeIn(frame, 35, 15),
            marginBottom: 8,
          }}>
            — {author}
          </p>
        )}
        
        {source && (
          <p style={{
            fontSize: 'clamp(14px, 1.8vw, 18px)',
            color: COLORS.gray,
            fontFamily: '"Noto Serif CJK SC", serif',
            opacity: fadeIn(frame, 45, 15),
          }}>
            {source}
          </p>
        )}
      </div>
    </Centered>
  );
}

/**
 * NumberHighlight - 数字强调
 * 用于：数据、统计、关键数字
 */
export function NumberHighlight({
  frame,
  title,
  stats = [],
  description,
}) {
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(135deg, ${COLORS.bg2}, ${COLORS.bg1})`,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '5%',
    }}>
      {title && (
        <h1 style={{
          fontSize: 'clamp(24px, 4vw, 40px)',
          color: COLORS.white,
          fontFamily: '"Noto Serif CJK SC", serif',
          marginBottom: 50,
          opacity: fadeIn(frame, 0, 15),
        }}>
          {title}
        </h1>
      )}
      
      <div style={{
        display: 'flex',
        gap: 50,
        marginBottom: 40,
      }}>
        {stats.map((stat, i) => (
          <div key={i} style={{
            textAlign: 'center',
            opacity: fadeIn(frame, 20 + i * 12, 15),
            transform: `scale(${popIn(frame, 20 + i * 12)})`,
          }}>
            <div style={{
              fontSize: 'clamp(48px, 8vw, 96px)',
              fontWeight: 'bold',
              color: stat.color || COLORS.accent2,
              fontFamily: '"Noto Serif CJK SC", serif',
              lineHeight: 1,
              marginBottom: 10,
            }}>
              {stat.value}
            </div>
            <div style={{
              fontSize: 'clamp(16px, 2.2vw, 22px)',
              color: COLORS.gray,
              fontFamily: '"Noto Serif CJK SC", serif',
            }}>
              {stat.label}
            </div>
          </div>
        ))}
      </div>
      
      {description && (
        <p style={{
          fontSize: 'clamp(16px, 2.2vw, 22px)',
          color: COLORS.lightGray,
          fontFamily: '"Noto Serif CJK SC", serif',
          textAlign: 'center',
          maxWidth: '70%',
          lineHeight: 1.8,
          opacity: fadeIn(frame, 50, 15),
        }}>
          {description}
        </p>
      )}
    </div>
  );
}

/**
 * ProcessFlow - 流程图布局
 * 用于：流程、循环、系统
 */
export function ProcessFlow({
  frame,
  title,
  steps = [],
  showArrows = true,
  loop = false,
}) {
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(180deg, ${COLORS.bg2}, ${COLORS.bg1})`,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '5%',
    }}>
      {title && (
        <h1 style={{
          fontSize: 'clamp(24px, 4vw, 40px)',
          color: COLORS.white,
          fontFamily: '"Noto Serif CJK SC", serif',
          marginBottom: 40,
          opacity: fadeIn(frame, 0, 15),
        }}>
          {title}
        </h1>
      )}
      
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 15,
        flexWrap: 'wrap',
        justifyContent: 'center',
      }}>
        {steps.map((step, i) => (
          <React.Fragment key={i}>
            <div style={{
              background: `${step.color}22`,
              borderRadius: 12,
              padding: '20px 30px',
              borderLeft: `4px solid ${step.color}`,
              opacity: fadeIn(frame, 15 + i * 12, 12),
              transform: `scale(${popIn(frame, 15 + i * 12)})`,
            }}>
              <div style={{
                fontSize: 'clamp(16px, 2.2vw, 22px)',
                color: COLORS.white,
                fontFamily: '"Noto Serif CJK SC", serif',
                fontWeight: 'bold',
              }}>
                {step.title}
              </div>
              {step.subtitle && (
                <div style={{
                  fontSize: 'clamp(12px, 1.6vw, 16px)',
                  color: COLORS.gray,
                  fontFamily: '"Noto Serif CJK SC", serif',
                  marginTop: 5,
                }}>
                  {step.subtitle}
                </div>
              )}
            </div>
            
            {showArrows && i < steps.length - 1 && (
              <div style={{
                color: COLORS.accent2,
                fontSize: 24,
                opacity: fadeIn(frame, 20 + i * 12, 10),
              }}>
                →
              </div>
            )}
            
            {loop && i === steps.length - 1 && (
              <div style={{
                color: COLORS.accent5,
                fontSize: 24,
                opacity: fadeIn(frame, 20 + i * 12, 10),
              }}>
                ↺
              </div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

/**
 * IconGrid - 图标网格
 * 用于：特性、功能、分类
 */
export function IconGrid({
  frame,
  title,
  items = [],
  columns = 3,
  itemDelay = 10,
}) {
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(135deg, ${COLORS.bg2}, ${COLORS.bg1})`,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '5%',
    }}>
      {title && (
        <h1 style={{
          fontSize: 'clamp(24px, 4vw, 40px)',
          color: COLORS.white,
          fontFamily: '"Noto Serif CJK SC", serif',
          marginBottom: 40,
          opacity: fadeIn(frame, 0, 15),
        }}>
          {title}
        </h1>
      )}
      
      <div style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gap: 30,
        maxWidth: '85%',
      }}>
        {items.map((item, i) => (
          <div key={i} style={{
            textAlign: 'center',
            opacity: fadeIn(frame, itemDelay + i * itemDelay, 12),
            transform: `scale(${popIn(frame, itemDelay + i * itemDelay)})`,
          }}>
            {item.icon && (
              <div style={{
                width: 60,
                height: 60,
                borderRadius: 12,
                background: `${item.color || COLORS.accent2}33`,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                margin: '0 auto 15px',
              }}>
                {item.icon}
              </div>
            )}
            <h3 style={{
              fontSize: 'clamp(16px, 2.2vw, 22px)',
              color: COLORS.white,
              fontFamily: '"Noto Serif CJK SC", serif',
              marginBottom: 8,
            }}>
              {item.title}
            </h3>
            {item.subtitle && (
              <p style={{
                fontSize: 'clamp(12px, 1.6vw, 16px)',
                color: COLORS.gray,
                fontFamily: '"Noto Serif CJK SC", serif',
                margin: 0,
              }}>
                {item.subtitle}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/**
 * SceneTitle - 场景标题
 * 用于：章节开头、过渡
 */
export function SceneTitle({
  frame,
  number,
  title,
  subtitle,
  color = COLORS.accent2,
}) {
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(135deg, ${COLORS.bg1}, ${COLORS.bg2})`,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      {number && (
        <div style={{
          fontSize: 'clamp(80px, 15vw, 180px)',
          fontWeight: 'bold',
          color: `${color}22`,
          fontFamily: '"Noto Serif CJK SC", serif',
          lineHeight: 1,
          opacity: fadeIn(frame, 0, 20),
          marginBottom: -40,
        }}>
          {number}
        </div>
      )}
      
      <h1 style={{
        fontSize: 'clamp(32px, 5vw, 56px)',
        color: COLORS.white,
        fontFamily: '"Noto Serif CJK SC", serif',
        textAlign: 'center',
        opacity: fadeIn(frame, 15, 20),
        marginBottom: 20,
      }}>
        {title}
      </h1>
      
      {subtitle && (
        <p style={{
          fontSize: 'clamp(16px, 2.5vw, 24px)',
          color: COLORS.gray,
          fontFamily: '"Noto Serif CJK SC", serif',
          textAlign: 'center',
          opacity: fadeIn(frame, 30, 15),
        }}>
          {subtitle}
        </p>
      )}
    </div>
  );
}

/**
 * TwoColumnList - 双栏列表
 * 用于：对比、分类
 */
export function TwoColumnList({
  frame,
  title,
  leftTitle,
  leftItems = [],
  rightTitle,
  rightItems = [],
  leftColor = COLORS.accent1,
  rightColor = COLORS.accent2,
}) {
  const renderList = (items, color, delay) => (
    <div>
      {items.map((item, i) => (
        <div key={i} style={{
          display: 'flex',
          alignItems: 'flex-start',
          gap: 12,
          marginBottom: 15,
          opacity: fadeIn(frame, delay + i * 10, 12),
        }}>
          <div style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: color,
            marginTop: 10,
            flexShrink: 0,
          }} />
          <p style={{
            fontSize: 'clamp(14px, 2vw, 20px)',
            color: COLORS.white,
            fontFamily: '"Noto Serif CJK SC", serif',
            lineHeight: 1.8,
            margin: 0,
          }}>
            {item}
          </p>
        </div>
      ))}
    </div>
  );
  
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: `linear-gradient(135deg, ${COLORS.bg2}, ${COLORS.bg1})`,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '5%',
    }}>
      {title && (
        <h1 style={{
          fontSize: 'clamp(24px, 4vw, 40px)',
          color: COLORS.white,
          fontFamily: '"Noto Serif CJK SC", serif',
          marginBottom: 40,
          opacity: fadeIn(frame, 0, 15),
        }}>
          {title}
        </h1>
      )}
      
      <div style={{
        display: 'flex',
        gap: 60,
        maxWidth: '90%',
      }}>
        <div style={{ flex: 1 }}>
          <h3 style={{
            fontSize: 'clamp(18px, 2.5vw, 26px)',
            color: leftColor,
            fontFamily: '"Noto Serif CJK SC", serif',
            marginBottom: 25,
            opacity: fadeIn(frame, 15, 15),
          }}>
            {leftTitle}
          </h3>
          {renderList(leftItems, leftColor, 25)}
        </div>
        
        <div style={{ flex: 1 }}>
          <h3 style={{
            fontSize: 'clamp(18px, 2.5vw, 26px)',
            color: rightColor,
            fontFamily: '"Noto Serif CJK SC", serif',
            marginBottom: 25,
            opacity: fadeIn(frame, 15, 15),
          }}>
            {rightTitle}
          </h3>
          {renderList(rightItems, rightColor, 25)}
        </div>
      </div>
    </div>
  );
}

// ===== 辅助组件 =====

export function TextBlock({ title, lines = [], frame, titleDelay = 0, lineDelay = 15 }) {
  return (
    <div>
      {title && (
        <h1 style={{
          fontSize: 'clamp(28px, 4.5vw, 48px)',
          color: COLORS.white,
          fontFamily: '"Noto Serif CJK SC", serif',
          marginBottom: 40,
          lineHeight: 1.4,
          opacity: fadeIn(frame, titleDelay, 15),
        }}>
          {title}
        </h1>
      )}
      {lines.map((line, i) => (
        <p key={i} style={{
          fontSize: 'clamp(16px, 2.5vw, 24px)',
          color: COLORS.white,
          fontFamily: '"Noto Serif CJK SC", serif',
          lineHeight: 2.4,
          marginBottom: 18,
          opacity: fadeIn(frame, titleDelay + lineDelay + i * lineDelay, 15),
          transform: `translateY(${slideUp(frame, titleDelay + lineDelay + i * lineDelay, 15, 12)}px)`,
        }}>
          {line}
        </p>
      ))}
    </div>
  );
}

export function IconBox({ children, color = COLORS.accent2, size = 60 }) {
  return (
    <div style={{
      width: size,
      height: size,
      borderRadius: 12,
      background: `${color}33`,
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      {children}
    </div>
  );
}

export function Card({ children, color = COLORS.accent2, frame, delay = 0 }) {
  return (
    <div style={{
      background: `linear-gradient(135deg, ${color}22, ${color}11)`,
      borderRadius: 20,
      padding: 30,
      opacity: fadeIn(frame, delay, 15),
    }}>
      {children}
    </div>
  );
}

export function DecorativeBackground({ type = 'stars', frame, count = 30, width, height }) {
  if (type === 'stars') {
    const stars = [];
    for (let i = 0; i < count; i++) {
      const x = (i * 137.5 * 7.3) % width;
      const y = (i * 137.5 * 13.7) % height;
      const twinkle = 0.3 + Math.sin(frame * 0.08 + i) * 0.3;
      stars.push(
        <div key={i} style={{
          position: 'absolute',
          left: x,
          top: y,
          width: 3,
          height: 3,
          borderRadius: '50%',
          background: COLORS.accent2,
          opacity: twinkle * fadeIn(frame, 0, 30),
        }} />
      );
    }
    return <>{stars}</>;
  }
  return null;
}

/**
 * 动画数字
 */
export function AnimatedNumber({ value, frame, startFrame = 20, duration = 30 }) {
  const numValue = parseFloat(value) || 0;
  const progress = fadeIn(frame, startFrame, duration);
  const displayValue = Math.round(numValue * progress);
  
  return <span>{displayValue}</span>;
}

// ===== 更多布局组件 =====

/**
 * LowerThird - 下三分之一布局
 * 用于：人物介绍、地点标注、字幕叠加
 */
export function LowerThird({
  frame,
  title,
  subtitle,
  position = 'left', // 'left' | 'center' | 'right'
  color = COLORS.accent2,
  children,
}) {
  const positionStyles = {
    left: { left: '5%', right: 'auto', transform: 'none' },
    center: { left: '50%', right: 'auto', transform: 'translateX(-50%)' },
    right: { right: '5%', left: 'auto', transform: 'none' },
  };
  
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      {children}
      
      <div style={{
        position: 'absolute',
        bottom: '8%',
        ...positionStyles[position],
        background: `linear-gradient(135deg, ${COLORS.bg1}ee, ${COLORS.bg2}ee)`,
        padding: '15px 25px',
        borderRadius: 8,
        borderLeft: `4px solid ${color}`,
        opacity: fadeIn(frame, 0, 15),
        backdropFilter: 'blur(10px)',
      }}>
        {title && (
          <div style={{
            fontSize: 'clamp(18px, 2.5vw, 26px)',
            color: COLORS.white,
            fontFamily: '"Noto Serif CJK SC", serif',
            fontWeight: 'bold',
          }}>
            {title}
          </div>
        )}
        {subtitle && (
          <div style={{
            fontSize: 'clamp(14px, 2vw, 18px)',
            color: color,
            fontFamily: '"Noto Serif CJK SC", serif',
            marginTop: 5,
          }}>
            {subtitle}
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * RuleOfThirds - 三分法布局
 * 用于：主次分明的场景，重要元素放在 1/3 或 2/3 位置
 */
export function RuleOfThirds({
  frame,
  mainContent,
  secondaryContent,
  mainPosition = 'right', // 'left' | 'right' | 'top' | 'bottom'
  mainRatio = 0.66, // 主内容占比
}) {
  const isVertical = mainPosition === 'top' || mainPosition === 'bottom';
  
  const containerStyle = {
    width: '100%',
    height: '100%',
    display: 'flex',
    flexDirection: isVertical ? 'column' : 'row',
  };
  
  const mainStyle = {
    flex: mainRatio,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  };
  
  const secondaryStyle = {
    flex: 1 - mainRatio,
    background: `${COLORS.bg2}66`,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 30,
  };
  
  // 根据位置调整顺序
  const mainFirst = mainPosition === 'left' || mainPosition === 'top';
  
  return (
    <div style={containerStyle}>
      {mainFirst ? (
        <>
          <div style={mainStyle}>
            {typeof mainContent === 'function' ? mainContent(frame) : mainContent}
          </div>
          <div style={secondaryStyle}>
            {typeof secondaryContent === 'function' ? secondaryContent(frame) : secondaryContent}
          </div>
        </>
      ) : (
        <>
          <div style={secondaryStyle}>
            {typeof secondaryContent === 'function' ? secondaryContent(frame) : secondaryContent}
          </div>
          <div style={mainStyle}>
            {typeof mainContent === 'function' ? mainContent(frame) : mainContent}
          </div>
        </>
      )}
    </div>
  );
}
