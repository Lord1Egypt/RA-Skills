# STM32 / Arduino FOC 参数配置代码示例

## 1. STM32 + HAL + 手动 FOC

```c
// motor_config.h
#ifndef __MOTOR_CONFIG_H
#define __MOTOR_CONFIG_H

// ==================== 电机参数（来自 parameter_id_flow.py）====================
#define MOTOR_POLE_PAIRS   4
#define MOTOR_RS           1.23f      // Ω @ 20℃
#define MOTOR_LD           5.6e-3f    // H
#define MOTOR_LQ           5.6e-3f    // H（表贴式）
#define MOTOR_KE           0.082f     // V/(rad/s)
#define MOTOR_KT           0.196f     // Nm/A（计算值）
#define MOTOR_FLUX         0.0104f    // Wb（Ψm = Ke/ωe）

// ==================== 电流环 PI ================================
typedef struct {
    float Kp;
    float Ki;
    float Kd;
    float out_max;
    float out_min;
} PI_Controller;

PI_Controller pi_id = {
    .Kp = MOTOR_RS * 0.5f,
    .Ki = MOTOR_RS / MOTOR_LD * Ts,
    .out_max = 10.0f,
    .out_min = -10.0f,
};

PI_Controller pi_iq = {
    .Kp = MOTOR_RS * 0.5f,
    .Ki = MOTOR_RS / MOTOR_LQ * Ts,
    .out_max = 10.0f,
    .out_min = -10.0f,
};

// ==================== 速度环 PI ================================
PI_Controller pi_speed = {
    .Kp = 0.5f,
    .Ki = 0.05f,
    .out_max = 15.0f,   // Iq 限幅 (A)
    .out_min = -15.0f,
};

// ==================== 速度环低通滤波 ============================
#define SPEED_FILTER_TAU   0.01f   // 滤波时间常数 (s)

// ==================== SVPWM 配置 ==============================
#define PWM_FREQUENCY      20000   // 20kHz PWM
#define VDC                48.0f   // 母线电压 V

// ==================== ADC 电流采样 ============================
#define RS_SHUNT           0.1f    // 采样电阻 Ω
#define OPAMP_GAIN         10.0f   // 运放增益
#define ADC_VREF           3.3f    // ADC 参考电压
#define ADC_MAX            4095    // 12-bit ADC

// 电流标定系数
#define CURRENT_SCALE      (ADC_VREF / ADC_MAX / RS_SHUNT / OPAMP_GAIN)

// ==================== 角度机械/电气 ============================
// 机械角度 → 电气角度
#define MECH_TO_ELEC(mech_angle)   ((mech_angle) * MOTOR_POLE_PAIRS)

// 电气角度（弧度）→ 机械角度（弧度）
#define ELEC_TO_MECH(elec_angle)   ((elec_angle) / MOTOR_POLE_PAIRS)

#endif
```

```c
// foc_controller.c
// FOC 电流环核心计算（每 PWM 周期执行一次）

// 输入：三相电流 ia, ib（第三相 ic = -ia-ib）
// 输入：转子电气角度 theta_e（来自编码器或 Hall）
// 输出：Ualpha, Ubeta（SVPWM 占空比）

void FOC_CurrentLoop(float ia, float ib, float theta_e,
                      float Id_ref, float Iq_ref,
                      float *Ualpha, float *Ubeta) {
    // 1. Clarke 变换（ia, ib → Ialpha, Ibeta）
    float Ialpha = ia;
    float Ibeta = (ia + 2.0f * ib) * 0.8660254f;

    // 2. Park 变换（Ialpha, Ibeta → Id, Iq）
    float cos_theta = arm_cos_f32(theta_e);
    float sin_theta = arm_sin_f32(theta_e);

    float Id = Ialpha * cos_theta + Ibeta * sin_theta;
    float Iq = -Ialpha * sin_theta + Ibeta * cos_theta;

    // 3. PI 控制（Id 环）
    float Vd = PI_Control(&pi_id, Id_ref, Id);

    // 4. PI 控制（Iq 环）
    float Vq = PI_Control(&pi_iq, Iq_ref, Iq);

    // 5. 反 Park 变换（Vd, Vq → Valpha, Vbeta）
    float Valpha = Vd * cos_theta - Vq * sin_theta;
    float Vbeta = Vd * sin_theta + Vq * cos_theta;

    // 6. 输出（后续接 SVPWM）
    *Ualpha = Valpha;
    *Ubeta = Vbeta;
}

float PI_Control(PI_Controller *pi, float ref, float fb) {
    float error = ref - fb;
    static float integral = 0;

    // 积分项（带积分限幅）
    integral += error * pi->Ki;
    if (integral > pi->out_max) integral = pi->out_max;
    if (integral < pi->out_min) integral = pi->out_min;

    // 输出
    float out = pi->Kp * error + integral;
    if (out > pi->out_max) out = pi->out_max;
    if (out < pi->out_min) out = pi->out_min;

    return out;
}
```

## 2. Arduino SimpleFOC 库配置

```cpp
// simplefoc_motor.ino
#include <SimpleFOC.h>

// ===== 电机实例 =====
BLDCMotor motor = BLDCMotor(POLE_PAIRS);
BLDCDriver3PWM driver = BLDCDriver3PWM(PWM_U, PWM_V, PWM_W, ENABLE_PIN);

// ===== 编码器（或 Hall 传感器）=====
Encoder encoder = Encoder(ENC_A, ENC_B, 500);
// 回调函数
void doA() { encoder.handleA(); }
void doB() { encoder.handleB(); }

// ===== 电流检测（可选）=====
// InlineCurrentSense 当前检测

void setup() {
    // 1. 初始化编码器
    encoder.init();
    encoder.enableInterrupts(doA, doB);
    motor.linkSensor(&encoder);

    // 2. 配置驱动
    driver.voltage_power_supply = 48;
    driver.voltage_limit = 36;  // PWM 限幅（保护电机）
    driver.init();
    motor.linkDriver(&driver);

    // 3. 配置电流检测（可选）
    // motor.linkCurrentSense(&cs);

    // 4. FOC 控制模式
    motor.controller = MotionControlType::torque;

    // ===== 电机参数（来自参数辨识）=====
    motor.phase_resistance = 1.23;   // Ω
    motor.phase_inductance = 5.6;   // mH（SimpleFOC 内部用 mH）
    motor.KV = 120;                 // KV = 1/Ke ≈ 1/0.082 ≈ 12 → 但这里用 rpm/V
                                    // 实际 KV = noload_rpm / V
    motor.pole_pairs = 4;
    motor.current_limit = 10;        // A（电流限幅）

    // 5. 速度环配置
    motor.velocity_limit = 3000;    // rpm
    motor.LPF_velocity.Tf = 0.01;   // 速度低通滤波 (s)

    // 6. 初始参数整定（可先用这个，后续手动微调）
    // SimpleFOC 提供 controller->PID_velocity、PID_current_d、PID_current_q
    motor.PID_velocity.P = 0.5;
    motor.PID_velocity.I = 0.1;
    motor.PID_velocity.D = 0.0;
    motor.PID_velocity.output_ramp = 1000;
    motor.PID_velocity.limit = 10;

    // 电流环（dq轴）
    motor.PID_current_d.P = motor.phase_resistance * 0.5;
    motor.PID_current_d.I = motor.phase_resistance / motor.phase_inductance * 0.001;
    motor.PID_current_q = motor.PID_current_d;  // 表贴式电机

    // 7. 初始化
    motor.init();
    motor.initFOC();

    Serial.begin(115200);
    Serial.println("FOC 初始化完成");
}

void loop() {
    // 必须高频调用
    motor.loopFOC();

    // ===== 速度控制模式 =====
    // 目标转速 rpm
    motor.move(1500);

    // 或力矩控制模式（直接给 q轴电流）
    // motor.move(current_q);

    // 串口调试
    if (millis() % 500 == 0) {
        Serial.print("Angle: "); Serial.print(motor.shaft_angle);
        Serial.print("  Speed: "); Serial.print(motor.shaft_velocity);
        Serial.print("  Vq: "); Serial.print(motor.voltage_q);
        Serial.println();
    }
}
```

## 3. STM32 + CubeMX + FreeRTOS + MC_SDK 兼容配置

```c
// main.c 中的电机参数结构体（MC_SDK 格式）

Motor_Parameters_t MotorParams = {
    .pole_pairs = 4,
    .rated_speed = 3000,          // rpm
    .rated_torque = 0.64,         // Nm
    .rated_voltage = 48,          // V
    .rated_current = 10,          // A

    // 电气参数
    .Rs = 1.23f,                 // Ω @ 20℃
    .Ls = 5.6e-3f,               // H
    .ke = 0.082f,                 // V/(rad/s)
    .kt = 0.196f,                 // Nm/A

    // 电流环
    .current_mode = CURRENT_MODE_FOC,
    .Id_ref = 0,                  // d轴电流参考（MTPA = 0）
    .Iq_ref = 5,                 // q轴电流参考（额定电流一半启动）

    // PI 参数
    .PI_parameters = {
        .Kp = 1.5f,
        .Ki = 0.05f,
        .Kd = 0,
        .output_limit = 10.0f,
    },
};

// 温度补偿
#define TEMP_COMPENSATION_ENABLED  1
#define MOTOR_TEMP_NOMINAL        25.0f   // ℃
#define MOTOR_TEMP_MAX            100.0f  // ℃
#define TEMP_COEFFICIENT          0.004f  // 铜温漂系数

// 运行时更新电阻（温度补偿）
void UpdateRsWithTemperature(float motor_temp_C) {
    float Rs_corrected = MotorParams.Rs *
        (1 + TEMP_COEFFICIENT * (motor_temp_C - MOTOR_TEMP_NOMINAL));
    // 更新 PI 控制器参数
    MC_PI_Update(&PI_Id, Rs_corrected, MotorParams.Ls);
}
```

## 4. 参数微调指南

```
现象               原因                调整方向
---------------------------------------------------------------
电流振荡           Kp 过大             减小 Kp
                   Ki 过大             减小 Ki
低速抖动           编码器分辨率低      提高速度环滤波（增大 Tf）
                   速度环带宽过高      减小速度环 P
高速失步           反电动势常数偏低    重新测量 Ke
                   电压裕量不足       提高 Vdc 或降转速
启动无力           Iq_ref 限幅过低     增大 Iq_ref 限幅
                   Rs 测量值偏大      重新测量电阻
定位精度差         Id≠0（凸极机）     检查 MTPA 控制
```

## 5. 常见故障代码

```
MC_NO_ERROR        无错误
MC_ERROR_FOC       FOC 计算错误
MC_ERROR_CUR       电流采样异常（检查运放接线）
MC_ERROR_SPD       速度检测异常（检查编码器 Z 信号）
MC_ERROR_OC        过流（检查功率管驱动）
MC_ERROR_OV        母线过压（检查制动电阻）
MC_ERROR_UV        母线欠压（检查电源）
MC_ERROR_NO        电机未连接（检查 UVW 接线）
```
