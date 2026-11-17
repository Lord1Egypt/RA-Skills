/**
 * stepper_28byj48.h - 28BYJ-48 步进电机 + ULN2003 驱动（可移植版）
 *
 * 适用：任何 MCU，只需在 stepper_28byj48_port.h 提供 4 路 GPIO + 延时
 * 特性：C99、无动态内存、步数/拍相/延时换算全为纯函数（PC 上可单元测试）
 *
 * 核心知识（新手最常算错的地方）：
 *   - 减速比精确值 63.68395:1（不是标称 64:1！）
 *   - 内部转子 32 全步/圈 → 输出轴精确 2038 全步/圈 或 4076 半步/圈
 *   - 网上代码几乎都写 2048/4096（按 64:1 算），一圈差 ~1.8°，
 *     云台/时钟类应用累计误差肉眼可见（详见 wiring.md 坑 2）
 *
 * 用法：
 *   int steps = stepper_angle_to_steps(90, 1);        // 90° 半步 → 1019 步
 *   for (int i = 0; i < steps; i++) {
 *       stepper_write_phase(stepper_phase_pattern(i, 1));
 *       stepper_delay_us(stepper_rpm_to_delay_us(15, 1));
 *   }
 *
 * 验证记录：见本目录 meta.json
 */
#ifndef STEPPER_28BYJ48_H
#define STEPPER_28BYJ48_H

#include <stdint.h>

/* ---- 移植适配层：在 stepper_28byj48_port.h 中实现 ---- */
#include <stepper_28byj48_port.h>  /* 提供 stepper_write_phase(pattern)
                                      stepper_delay_us(us) */

/* 每圈步数（精确减速比 63.68395:1，转子 32 步/圈）。
 * 纯函数。halfstep 非 0 → 4076 半步/圈；0 → 2038 全步/圈。 */
int stepper_steps_per_rev(int halfstep);

/* 角度 → 步数（四舍五入）。纯函数。
 * angle 可负（反向），halfstep 非 0 用半步分辨率。 */
int stepper_angle_to_steps(int angle, int halfstep);

/* 第 idx 拍的相序输出（bit0=IN1 ... bit3=IN4）。纯函数。
 * halfstep 非 0 → 8 拍序列（idx 对 8 取模）；否则 4 拍（对 4 取模）。 */
int stepper_phase_pattern(int idx, int halfstep);

/* 目标转速 → 单步延时（微秒）。纯函数。
 * rpm<=0 → -1；rpm>18（超转矩能力，实用上限约 15）→ -2。 */
int stepper_rpm_to_delay_us(int rpm, int halfstep);

#endif /* STEPPER_28BYJ48_H */
