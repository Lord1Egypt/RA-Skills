---
name: ai-robotics
description: AI机器人指南 — 机器人类型(工业/服务/协作/人形/无人机)/运动学(正/逆运动学)/ROS机器人操作系统/传感器(LiDAR/IMU/视觉/力觉)/执行器(伺服/步进/液压)/SLAM即时定位建图/路径规划(A*/RRT)/控制理论(PID/MPC)/机器人编程(Python/C++/URDF)/机器人伦理/四足机器人/波士顿动力/人形机器人(Atlas/Optimus)/工业机器人(KUKA/FANUC/ABB)/机器人竞赛(RoboMaster/FRC)。全球千亿美元产业，ClawHub零覆盖。
author: ai-gaoqian
tags: [robotics, ros, slam, kinematics, pid-control, drone, quadruped, humanoid]
---

# AI机器人指南

从运动学到人形机器人。ROS/SLAM/控制全覆盖。

## 核心能力

### 1. 机器人入门
- **机器人三要素**：感知Sense(传感器)→规划Plan(算法)→行动Act(执行器)
- **类型**：工业机器人(焊接/装配/重/快/精准)→服务机器人(扫地/送餐/导览)→协作机器人Cobot(和人一起工作/安全)→人形机器人(仿人/Atlas/Optimus)→无人机(四旋翼/固定翼)→四足机器人(Spot/机器狗)
- **机器人=机械结构+电子+软件**：三者缺一不可
- **自由度DOF**：机器人的运动维度/6DOF=3个位置+3个方向(人类手臂就是6DOF)
- **末端执行器End Effector**：机器人手/夹爪/吸盘/焊枪/喷涂枪
- **工作空间Workspace**：机器人末端能到达的所有点的集合

### 2. 运动学Kinematics
- **正运动学Forward Kinematics**：已知关节角度→求末端位置和姿态(直接算)
- **逆运动学Inverse Kinematics(IK)**：已知想要的末端位置和姿态→求关节角度(要解方程/可能有多个解/可能无解)
- **DH参数Denavit-Hartenberg**：描述机器人连杆和关节的标准方法/四个参数(θ/d/a/α)
- **雅可比矩阵Jacobian**：关节速度→末端速度的映射/奇点问题
- **工作空间分析**：画可达工作空间/检测奇异性
- **运动学仿真工具**：ROS+RViz/Gazebo/MATLAB Robotics Toolbox

### 3. ROS(机器人操作系统)
- **ROS不是真正的OS**：是分布式框架/节点Node之间通过消息Message通信
- **核心概念**：节点Node(进程)/话题Topic(发布订阅)/服务Service(请求回复)/动作Action(长期任务+反馈)
- **核心包**：roscore(核心)/rviz(可视化)/gazebo(仿真)/tf(坐标变换)/moveit(运动规划)
- **SLAM包**：gmapping(2D激光)/cartographer(Google的2D/3D)/RTAB-Map(RGB-D)
- **导航栈Navigation Stack**：全局规划器global_planner+局部规划器local_planner+代价地图costmap
- **ROS2**：ROS1的后继/支持多机器人/实时性更好/DDS通信/ROS1在2025年已停止维护

### 4. 传感器
- **LiDAR激光雷达**：发射激光/测距/3D点云/自动驾驶必备/Velodyne/Ouster/Hesai
- **视觉传感器**：单目相机(2D→3D难)/双目相机(测距)/RGB-D深度相机(Intel RealSense/Kinect)
- **IMU惯性测量单元**：加速度计+陀螺仪+磁力计/姿态估计/漂移问题
- **力/力矩传感器**：六维力传感器/精确力控/拖动示教
- **编码器Encoder**：关节角度/电机转速/最基础传感器
- **传感器融合**：卡尔曼滤波(线性)/扩展卡尔曼滤波EKF(非线性)/粒子滤波

### 5. SLAM(即时定位与建图)
- **SLAM问题**：机器人不知道自己在哪/也不知道地图什么样/同时求解两个问题
- **视觉SLAM**：ORB-SLAM3(特征点法)/DSO(直接法)/单目/双目/RGB-D
- **激光SLAM**：2D激光(EKF-SLAM/FastSLAM)→3D激光(LOAM/Lego-LOAM)
- **前端vs后端**：前端=特征提取+数据关联/后端=图优化+闭环检测
- **闭环检测Loop Closure**：机器人回到走过的地方→认出→消除累积误差(核心!)
- **语义SLAM**：SLAM+物体识别/更鲁棒

### 6. 路径规划与控制
- **全局规划**：A*(启发式搜索/最常用)/Dijkstra(没启发/慢)/RRT(快速随机树/高维空间好用)
- **局部规划**：DWA动态窗口法(速度空间采样)/TEB时间弹性带
- **PID控制(经典中的经典！)**：P比例(现在误差)/I积分(过去累积误差)/D微分(预测未来趋势)/调参=经验+Ziegler-Nichols
- **前馈+反馈**：前馈=预测/反馈=修正/两者结合
- **自适应控制**：参数随时间自己调整/MPC模型预测控制(对未来N步优化)
- **力控vs位控**：位控=精确位置/力控=顺应环境(装配/打磨)/阻抗控制

### 7. 机器人大师
- **波士顿动力Boston Dynamics**：Spot(四足/商业)/Atlas(人形/液压/跑酷)/Handle(轮式)。
- **特斯拉Optimus**：人形/2022发布/目标=通用机器人/有望平价
- **Figure AI**：Figure 01→02/OpenAI合作/目标是"机器人劳动力"
- **工业四巨头**：FANUC(日本/黄)/KUKA(德国/橙/被美的收购)/ABB(瑞士)/Yaskawa安川(日本)
- **大疆DJI**：RoboMaster(机器人竞赛+教育)/无人机霸主/进入机器人底盘
- **宇树Unitree**：杭州/四足机器狗(价格亲民/H1人形也发布了)

### 8. 入门实战
- **新手推荐路径**：Python基础→ROS2入门→TurtleBot3仿真→Gazebo仿真→买个小四足/机械臂实物
- **仿真环境不花钱**：Gazebo(物理仿真)/Webots(开源)/CoppeliaSim(前V-REP)/Isaac Sim(NVIDIA)
- **第一台机器人**：TurtleBot3(差速底盘+LiDAR+相机)/约3000-5000元
- **机械臂入门**：uArm/Mirobot/越疆Dobot
- **竞赛**：RoboMaster(大疆/最酷的机器人比赛)/FRC(美国高中生)/RoboCup(机器人足球)
- **开源社区**：ros.org/ROS Discourse/GitHub

## 使用方式
描述需求，例如：
- "想学机器人，从哪开始？"
- "逆运动学怎么解？"
- "SLAM选激光还是视觉？"

## 适用人群
- 机器人入门
- ROS开发
- 仿真与实物
- 学术研究
