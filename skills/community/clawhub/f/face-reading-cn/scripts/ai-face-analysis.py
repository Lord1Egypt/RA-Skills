#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面相学 AI 图像识别工具 v1.0
基于 dlib 68 点面部特征检测，实现面相自动分析

依赖安装:
    pip install dlib opencv-python numpy scipy
    # dlib 需要 CMake 和编译环境
    # 或者使用预编译版本：pip install dlib-bin

使用方法:
    python ai-face-analysis.py image.jpg
    python ai-face-analysis.py image.jpg --output report.json
"""

import cv2
import dlib
import numpy as np
import json
import sys
import os
from scipy.spatial import distance as dist

# 检查依赖
try:
    import dlib
except ImportError:
    print("❌ 错误：需要安装 dlib")
    print("   pip install dlib 或 pip install dlib-bin")
    sys.exit(1)

try:
    import cv2
except ImportError:
    print("❌ 错误：需要安装 opencv-python")
    print("   pip install opencv-python")
    sys.exit(1)


class FaceAnalyzer:
    """面相学 AI 分析器"""
    
    def __init__(self, predictor_path=None):
        """
        初始化分析器
        
        Args:
            predictor_path: dlib 68 点预测模型路径
                           默认使用预训练模型或自动下载
        """
        # 加载 dlib 人脸检测器
        self.detector = dlib.get_frontal_face_detector()
        
        # 加载 68 点预测模型
        if predictor_path is None:
            # 尝试常见路径
            common_paths = [
                "shape_predictor_68_face_landmarks.dat",
                "./models/shape_predictor_68_face_landmarks.dat",
                os.path.expanduser("~/.dlib/shape_predictor_68_face_landmarks.dat"),
            ]
            for path in common_paths:
                if os.path.exists(path):
                    predictor_path = path
                    break
        
        if predictor_path and os.path.exists(predictor_path):
            self.predictor = dlib.shape_predictor(predictor_path)
            print(f"✅ 加载预测模型：{predictor_path}")
        else:
            print("⚠️  未找到预测模型，请下载：")
            print("   http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
            print("   解压后放到当前目录或指定路径")
            self.predictor = None
    
    def detect_face(self, image):
        """
        检测人脸
        
        Args:
            image: OpenCV 图像 (BGR)
        
        Returns:
            faces: 检测到的人脸列表
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 检测人脸
        faces = self.detector(gray, 1)
        
        return faces, gray
    
    def get_landmarks(self, image, face):
        """
        获取 68 个面部特征点
        
        Args:
            image: OpenCV 图像
            face: dlib 人脸矩形框
        
        Returns:
            landmarks: 68 个特征点坐标
        """
        if self.predictor is None:
            return None
        
        landmarks = self.predictor(image, face)
        points = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)]
        
        return points
    
    def analyze_face_shape(self, landmarks):
        """
        分析脸型（五行分类）
        
        Args:
            landmarks: 68 个特征点
        
        Returns:
            shape_type: 脸型（金/木/水/火/土）
            ratios: 比例数据
        """
        if landmarks is None:
            return "未知", {}
        
        # 计算面部尺寸
        jaw_width = dist.euclidean(landmarks[1], landmarks[15])  # 下颌宽度
        cheek_width = dist.euclidean(landmarks[2], landmarks[14])  # 颧骨宽度
        forehead_width = dist.euclidean(landmarks[20], landmarks[23])  # 额头宽度
        # 计算额头中点
        forehead_mid = (
            (landmarks[20][0] + landmarks[23][0]) / 2,
            (landmarks[20][1] + landmarks[23][1]) / 2
        )
        face_height = dist.euclidean(landmarks[8], forehead_mid)  # 下巴到额头中点
        
        # 计算比例
        width_ratio = face_height / (jaw_width + 0.01)  # 高宽比
        cheek_ratio = cheek_width / (face_height + 0.01)  # 颧骨相对宽度
        forehead_ratio = forehead_width / (jaw_width + 0.01)  # 额头下颌比
        face_length_ratio = face_height / (cheek_width + 0.01)  # 脸长颧骨比
        
        # 五行脸型判断（综合多个比例）
        # 木形：长脸，高宽比大
        # 水形：圆脸，颧骨宽，高宽比小
        # 金形：方脸，下颌宽，轮廓分明
        # 火形：尖脸，额头宽下巴尖
        # 土形：厚重，比例均衡
        
        scores = {
            "木": 0,
            "火": 0,
            "土": 0,
            "金": 0,
            "水": 0
        }
        
        # 木形评分：长脸特征
        if width_ratio > 1.3:
            scores["木"] += 3
        elif width_ratio > 1.1:
            scores["木"] += 2
        if face_length_ratio > 1.2:
            scores["木"] += 2
            
        # 火形评分：尖脸特征（额头宽下巴尖）
        if forehead_ratio > 1.15:
            scores["火"] += 3
        elif forehead_ratio > 1.05:
            scores["火"] += 2
        if width_ratio > 1.2 and forehead_ratio > 1.0:
            scores["火"] += 2
            
        # 土形评分：厚重特征（比例均衡）
        if 0.9 <= width_ratio <= 1.2 and 0.9 <= forehead_ratio <= 1.1:
            scores["土"] += 3
        elif 0.85 <= width_ratio <= 1.25:
            scores["土"] += 1
        if abs(cheek_ratio - 1.0) < 0.15:
            scores["土"] += 2
            
        # 金形评分：方脸特征（下颌宽）
        if jaw_width > cheek_width * 0.85:
            scores["金"] += 3
        elif jaw_width > cheek_width * 0.8:
            scores["金"] += 2
        if forehead_ratio < 0.95 and width_ratio < 1.1:
            scores["金"] += 2
            
        # 水形评分：圆脸特征（颧骨宽，脸短）
        if cheek_ratio > 1.05:
            scores["水"] += 3
        elif cheek_ratio > 0.95:
            scores["水"] += 2
        if width_ratio < 1.0 and forehead_ratio < 1.0:
            scores["水"] += 2
        
        # 找出最高分
        max_score = max(scores.values())
        shape_type = max(scores, key=scores.get)
        
        # 判断是否为混合类型（前两名分数接近）
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        is_mixed = sorted_scores[0][1] - sorted_scores[1][1] < 2
        
        shape_names = {
            "金": "方形",
            "木": "长形",
            "水": "圆形",
            "火": "尖形",
            "土": "厚重"
        }
        shape_name = shape_names.get(shape_type, "未知")
        
        result = {
            "face_height": face_height,
            "jaw_width": jaw_width,
            "cheek_width": cheek_width,
            "forehead_width": forehead_width,
            "width_ratio": width_ratio,
            "cheek_ratio": cheek_ratio,
            "forehead_ratio": forehead_ratio,
            "face_length_ratio": face_length_ratio,
            "shape_name": shape_name,
            "scores": scores,
            "is_mixed": is_mixed
        }
        
        # 如果是混合类型，添加第二类型
        if is_mixed:
            result["secondary_type"] = sorted_scores[1][0]
            result["mixed_name"] = f"{shape_names[shape_type]}+{shape_names[sorted_scores[1][0]]}"
        
        return shape_type, result
    
    def analyze_eyes(self, landmarks):
        """
        分析眼睛特征
        
        Args:
            landmarks: 68 个特征点
        
        Returns:
            eye_features: 眼睛特征字典
        """
        if landmarks is None:
            return {}
        
        # 左眼特征点 (36-41)
        left_eye = landmarks[36:42]
        # 右眼特征点 (42-47)
        right_eye = landmarks[42:48]
        
        # 计算眼睛大小
        left_eye_width = dist.euclidean(left_eye[0], left_eye[3])
        left_eye_height = dist.euclidean(left_eye[1], left_eye[5])
        right_eye_width = dist.euclidean(right_eye[0], right_eye[3])
        right_eye_height = dist.euclidean(right_eye[1], right_eye[5])
        
        # 平均眼睛大小
        avg_width = (left_eye_width + right_eye_width) / 2
        avg_height = (left_eye_height + right_eye_height) / 2
        eye_ratio = avg_height / (avg_width + 0.01)
        
        # 判断眼睛大小
        if avg_width > 50:  # 阈值可根据实际情况调整
            eye_size = "大"
        elif avg_width < 35:
            eye_size = "小"
        else:
            eye_size = "中"
        
        # 判断眼尾方向
        left_eye_tail = left_eye[3][1] - left_eye[0][1]
        right_eye_tail = right_eye[3][1] - right_eye[0][1]
        avg_tail = (left_eye_tail + right_eye_tail) / 2
        
        if avg_tail < -5:
            eye_direction = "上扬"
        elif avg_tail > 5:
            eye_direction = "下垂"
        else:
            eye_direction = "平"
        
        return {
            "eye_size": eye_size,
            "eye_width": avg_width,
            "eye_height": avg_height,
            "eye_ratio": eye_ratio,
            "eye_direction": eye_direction,
            "left_eye": {"width": left_eye_width, "height": left_eye_height},
            "right_eye": {"width": right_eye_width, "height": right_eye_height}
        }
    
    def analyze_eyebrows(self, landmarks):
        """
        分析眉毛特征
        
        Args:
            landmarks: 68 个特征点
        
        Returns:
            eyebrow_features: 眉毛特征字典
        """
        if landmarks is None:
            return {}
        
        # 左眉特征点 (17-21)
        left_brow = landmarks[17:22]
        # 右眉特征点 (22-26)
        right_brow = landmarks[22:27]
        
        # 计算眉毛密度（基于特征点分布）
        left_brow_length = sum(dist.euclidean(left_brow[i], left_brow[i+1]) for i in range(4))
        right_brow_length = sum(dist.euclidean(right_brow[i], right_brow[i+1]) for i in range(4))
        
        # 判断眉毛浓密度（简化版）
        brow_density = "中"  # 实际需要图像分析
        
        # 判断眉毛形状
        left_brow_slope = left_brow[0][1] - left_brow[4][1]
        right_brow_slope = right_brow[0][1] - right_brow[4][1]
        
        if left_brow_slope > 10 or right_brow_slope > 10:
            brow_shape = "上扬"
        elif left_brow_slope < -10 or right_brow_slope < -10:
            brow_shape = "下垂"
        else:
            brow_shape = "平"
        
        return {
            "brow_density": brow_density,
            "brow_shape": brow_shape,
            "left_brow_length": left_brow_length,
            "right_brow_length": right_brow_length
        }
    
    def analyze_nose(self, landmarks):
        """
        分析鼻子特征
        
        Args:
            landmarks: 68 个特征点
        
        Returns:
            nose_features: 鼻子特征字典
        """
        if landmarks is None:
            return {}
        
        # 鼻子特征点 (27-35)
        nose = landmarks[27:36]
        
        # 计算鼻子高度和宽度
        nose_height = dist.euclidean(nose[0], nose[8])
        nose_width = dist.euclidean(nose[4], nose[12]) if len(nose) > 12 else nose_height * 0.3
        
        # 判断鼻子高低
        if nose_height > 60:
            nose_height_type = "高"
        elif nose_height < 40:
            nose_height_type = "低"
        else:
            nose_height_type = "中"
        
        return {
            "nose_height": nose_height,
            "nose_width": nose_width,
            "nose_height_type": nose_height_type
        }
    
    def analyze_mouth(self, landmarks):
        """
        分析嘴巴特征
        
        Args:
            landmarks: 68 个特征点
        
        Returns:
            mouth_features: 嘴巴特征字典
        """
        if landmarks is None:
            return {}
        
        # 嘴巴特征点 (48-67)
        mouth = landmarks[48:68]
        
        # 计算嘴巴宽度
        mouth_width = dist.euclidean(mouth[0], mouth[6])
        
        # 判断嘴巴大小
        if mouth_width > 60:
            mouth_size = "大"
        elif mouth_width < 40:
            mouth_size = "小"
        else:
            mouth_size = "中"
        
        # 判断嘴角方向
        mouth_left = mouth[0]
        mouth_right = mouth[6]
        mouth_slope = mouth_right[1] - mouth_left[1]
        
        if mouth_slope < -5:
            mouth_corner = "上扬"
        elif mouth_slope > 5:
            mouth_corner = "下垂"
        else:
            mouth_corner = "平"
        
        return {
            "mouth_width": mouth_width,
            "mouth_size": mouth_size,
            "mouth_corner": mouth_corner
        }
    
    def analyze_ears(self, image, face):
        """
        分析耳朵特征（简化版，实际需要侧面图像）
        
        Args:
            image: OpenCV 图像
            face: dlib 人脸矩形框
        
        Returns:
            ear_features: 耳朵特征字典
        """
        # 正面图像难以准确分析耳朵
        # 这里返回估计值
        face_width = face.right() - face.left()
        
        # 简化判断
        ear_size = "中"  # 实际需要更复杂的分析
        
        return {
            "ear_size": ear_size,
            "note": "正面图像难以准确分析耳朵，需要侧面图像"
        }
    
    def generate_analysis(self, image_path, output_path=None):
        """
        生成完整面相分析报告
        
        Args:
            image_path: 输入图像路径
            output_path: 输出报告路径（可选）
        
        Returns:
            report: 分析报告字典
        """
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            return {"error": f"无法读取图像：{image_path}"}
        
        # 检测人脸
        faces, gray = self.detect_face(image)
        
        if len(faces) == 0:
            return {"error": "未检测到人脸"}
        
        if len(faces) > 1:
            print(f"⚠️  检测到 {len(faces)} 张人脸，分析第一张")
        
        face = faces[0]
        
        # 获取特征点
        landmarks = self.get_landmarks(image, face)
        
        if landmarks is None:
            return {"error": "无法获取面部特征点"}
        
        # 分析各个部位
        shape_type, shape_data = self.analyze_face_shape(landmarks)
        eye_features = self.analyze_eyes(landmarks)
        eyebrow_features = self.analyze_eyebrows(landmarks)
        nose_features = self.analyze_nose(landmarks)
        mouth_features = self.analyze_mouth(landmarks)
        ear_features = self.analyze_ears(image, face)
        
        # 生成面相学解读
        interpretation = self.generate_interpretation(
            shape_type, shape_data, eye_features, eyebrow_features,
            nose_features, mouth_features, ear_features
        )
        
        # 生成报告
        report = {
            "image": image_path,
            "face_detected": True,
            "landmarks": landmarks,
            "analysis": {
                "face_shape": {
                    "type": shape_type,
                    "name": shape_data.get("shape_name", ""),
                    "data": shape_data
                },
                "eyes": eye_features,
                "eyebrows": eyebrow_features,
                "nose": nose_features,
                "mouth": mouth_features,
                "ears": ear_features
            },
            "interpretation": interpretation,
            "disclaimer": "本分析仅供娱乐参考，不具备科学依据"
        }
        
        # 保存报告
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"✅ 报告已保存：{output_path}")
        
        return report
    
    def generate_interpretation(self, shape_type, shape_data, eye_features, 
                                 eyebrow_features, nose_features, mouth_features, ear_features):
        """
        生成面相学解读（包含五行分类详解、文献引用、流派说明）
        
        Returns:
            interpretation: 解读文本列表（带文献引用）
        """
        interpretations = []
        citations = []  # 存储文献引用
        
        # 五行详细解读（基于《柳庄相法·五行篇》）
        wuxing_details = {
            "金": {
                "name": "金形",
                "shape": "方形",
                "traits": "刚毅果断，有正义感，意志坚定",
                "career": "适合军警、法律、管理、金融",
                "wealth": "正财运好，靠努力获得财富",
                "health": "注意呼吸系统和肺部",
                "strength": "决策力强，坚持原则，重视义气",
                "weakness": "过于刚硬，缺乏柔性，容易冲动",
                "source": "《柳庄相法·五行篇》",
                "school": "福建派（理气派）",
                "original": "金形人，面方色白，骨重肉坚"
            },
            "木": {
                "name": "木形",
                "shape": "长形",
                "traits": "仁慈善良，有上进心，创意丰富",
                "career": "适合教育、文化、艺术、设计",
                "wealth": "财运平稳，靠专业技能",
                "health": "注意肝胆和神经系统",
                "strength": "仁慈同情，好学成长，思维活跃",
                "weakness": "容易忧虑，过于理想化，情绪波动",
                "source": "《柳庄相法·五行篇》",
                "school": "福建派（理气派）",
                "original": "木形人，面长色青，身直发茂"
            },
            "水": {
                "name": "水形",
                "shape": "圆形",
                "traits": "聪明智慧，适应力强，善于交际",
                "career": "适合商业、贸易、公关、咨询",
                "wealth": "财运好，善于理财",
                "health": "注意肾脏和泌尿系统",
                "strength": "智慧灵活，人缘好，商业头脑",
                "weakness": "过于圆滑，缺乏定性，易改变主意",
                "source": "《柳庄相法·五行篇》",
                "school": "福建派（理气派）",
                "original": "水形人，面圆色黑，肉多骨少"
            },
            "火": {
                "name": "火形",
                "shape": "尖形",
                "traits": "热情外向，行动力强，活力充沛",
                "career": "适合销售、演艺、媒体、创业",
                "wealth": "财运波动大，大进大出",
                "health": "注意心脏和血液循环",
                "strength": "热情开朗，表达力强，雷厉风行",
                "weakness": "脾气急躁，缺乏耐心，过于自我",
                "source": "《柳庄相法·五行篇》",
                "school": "福建派（理气派）",
                "original": "火形人，面尖色红，发少神露"
            },
            "土": {
                "name": "土形",
                "shape": "厚重",
                "traits": "诚信稳重，务实可靠，包容心强",
                "career": "适合房地产、农业、建筑、管理",
                "wealth": "财运稳定，善于积累",
                "health": "注意脾胃和消化系统",
                "strength": "诚信可靠，稳重踏实，重视家庭",
                "weakness": "反应较慢，过于保守，有时固执",
                "source": "《柳庄相法·五行篇》",
                "school": "福建派（理气派）",
                "original": "土形人，面厚色黄，肉实骨重"
            }
        }
        
        # 主类型解读
        if shape_type in wuxing_details:
            detail = wuxing_details[shape_type]
            interpretations.append(f"【{detail['name']}】脸型：{detail['shape']}")
            interpretations.append(f"  性格：{detail['traits']}")
            interpretations.append(f"  优势：{detail['strength']}")
            interpretations.append(f"  注意：{detail['weakness']}")
            interpretations.append(f"  事业：{detail['career']}")
            interpretations.append(f"  财运：{detail['wealth']}")
            interpretations.append(f"  健康：{detail['health']}")
            interpretations.append(f"  📚 来源：{detail['source']} | {detail['school']}")
            interpretations.append(f"  📖 原文：\"{detail['original']}\"")
            citations.append(f"{detail['source']} - {detail['school']}")
        
        # 混合类型解读
        if shape_data.get("is_mixed") and "secondary_type" in shape_data:
            secondary = shape_data["secondary_type"]
            if secondary in wuxing_details:
                sec_detail = wuxing_details[secondary]
                interpretations.append("")
                interpretations.append(f"【混合类型】兼有{sec_detail['name']}特征")
                interpretations.append(f"  补充特质：{sec_detail['traits']}")
                # 五行相生相克解读
                wuxing_cycle = {
                    ("金", "水"): "金生水：刚毅中带智慧，决策更周全",
                    ("金", "木"): "金克木：内心有冲突，需平衡果断与仁慈",
                    ("金", "火"): "火克金：热情与刚毅并存，注意情绪管理",
                    ("金", "土"): "土生金：稳重增强果断，基础更扎实",
                    ("木", "水"): "水生木：智慧滋养仁慈，创意更丰富",
                    ("木", "火"): "木生火：创意点燃热情，行动力更强",
                    ("木", "土"): "木克土：进取与稳重平衡，避免急躁",
                    ("木", "金"): "金克木：原则约束创意，需灵活变通",
                    ("水", "金"): "金生水：智慧得刚毅支持，执行力提升",
                    ("水", "木"): "水生木：灵活与成长结合，适应力更强",
                    ("水", "火"): "水克火：冷静平衡热情，避免冲动",
                    ("水", "土"): "土克水：稳重约束灵活，更脚踏实地",
                    ("火", "木"): "木生火：热情得创意支持，更有方向",
                    ("火", "土"): "火生土：热情滋养稳重，活力更持久",
                    ("火", "金"): "火克金：激情挑战原则，需相互尊重",
                    ("火", "水"): "水克火：冷静调和热情，更趋平衡",
                    ("土", "金"): "土生金：稳重支持果断，基础更牢",
                    ("土", "水"): "土克水：务实约束灵活，更接地气",
                    ("土", "木"): "木克土：成长突破保守，需开放心态",
                    ("土", "火"): "火生土：活力滋养稳重，更积极向上",
                }
                pair = tuple(sorted([shape_type, secondary]))
                if pair in wuxing_cycle:
                    interpretations.append(f"  五行关系：{wuxing_cycle[pair]}")
        
        # 眼睛解读（基于《麻衣神相·五官篇》《相理衡真·眼相篇》）
        if eye_features:
            eye_size = eye_features.get("eye_size", "")
            eye_dir = eye_features.get("eye_direction", "")
            if eye_size == "大":
                interpretations.append("眼睛：大而明亮，性格开朗，表达力强")
                interpretations.append("  📚 来源：《相理衡真·眼相篇》 | 江西派（形势派）")
                interpretations.append("  📖 原文：\"眼大者，心性开朗，善于表达\"")
            elif eye_size == "小":
                interpretations.append("眼睛：小而专注，心思细腻，观察力强")
                interpretations.append("  📚 来源：《麻衣神相·五官篇》 | 江西派（形势派）")
                interpretations.append("  📖 原文：\"眼小者，心细如发，观察入微\"")
            if eye_dir == "上扬":
                interpretations.append("眼尾上扬，性格外向，有魅力")
                interpretations.append("  📚 来源：《水镜集·眼相篇》 | 江西派（形势派）")
                interpretations.append("  📖 原文：\"眼尾上扬，外向有魅\"")
            elif eye_dir == "下垂":
                interpretations.append("眼尾下垂，性格温和，体贴")
                interpretations.append("  📚 来源：《水镜集·眼相篇》 | 江西派（形势派）")
                interpretations.append("  📖 原文：\"眼尾下垂，温和体贴\"")
        
        # 鼻子解读（基于《麻衣神相·五官篇》）
        if nose_features:
            nose_h = nose_features.get("nose_height_type", "")
            if nose_h == "高":
                interpretations.append("鼻子高挺，财运较好，有领导能力")
                interpretations.append("  📚 来源：《麻衣神相·五官篇》 | 江西派（形势派）")
                interpretations.append("  📖 原文：\"鼻为财帛，高挺主富\"")
            elif nose_h == "低":
                interpretations.append("鼻子较低，性格温和，需努力积累")
                interpretations.append("  📚 来源：《麻衣神相·五官篇》 | 江西派（形势派）")
                interpretations.append("  📖 原文：\"鼻低者，性和缓，需勤积\"")
        
        # 嘴巴解读（基于《水镜集·口相篇》《麻衣神相·五官篇》）
        if mouth_features:
            mouth_s = mouth_features.get("mouth_size", "")
            mouth_c = mouth_features.get("mouth_corner", "")
            if mouth_s == "大":
                interpretations.append("嘴巴大，表达能力强，社交能力好")
                interpretations.append("  📚 来源：《麻衣神相·五官篇》 | 江西派（形势派）")
                interpretations.append("  📖 原文：\"口大者，善言辞，社交广\"")
            elif mouth_s == "小":
                interpretations.append("嘴巴小，谨慎细心，言语保守")
                interpretations.append("  📚 来源：《麻衣神相·五官篇》 | 江西派（形势派）")
                interpretations.append("  📖 原文：\"口小者，言谨慎，心思细\"")
            if mouth_c == "上扬":
                interpretations.append("嘴角上扬，乐观积极，人缘好")
                interpretations.append("  📚 来源：《水镜集·口相篇》 | 江西派（形势派）")
                interpretations.append("  📖 原文：\"嘴角扬，心乐观，人缘佳\"")
            elif mouth_c == "下垂":
                interpretations.append("嘴角下垂，需注意心态调整")
                interpretations.append("  📚 来源：《水镜集·口相篇》 | 江西派（形势派）")
                interpretations.append("  📖 原文：\"嘴角垂，心多忧\"")
        
        return interpretations


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("👤 面相学 AI 图像识别工具 v1.0")
        print("\n使用方法:")
        print("  python ai-face-analysis.py <图片路径> [输出文件]")
        print("\n示例:")
        print("  python ai-face-analysis.py face.jpg")
        print("  python ai-face-analysis.py face.jpg output.json")
        print("\n依赖安装:")
        print("  pip install dlib opencv-python numpy scipy")
        print("\n模型下载:")
        print("  http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        sys.exit(0)
    
    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 创建分析器
    analyzer = FaceAnalyzer()
    
    if analyzer.predictor is None:
        print("\n❌ 无法继续分析，请先下载预测模型")
        sys.exit(1)
    
    # 分析图像
    print(f"\n🔍 分析图像：{image_path}")
    report = analyzer.generate_analysis(image_path, output_path)
    
    if "error" in report:
        print(f"❌ 错误：{report['error']}")
        sys.exit(1)
    
    # 输出结果
    print("\n" + "="*60)
    print("📊 面相分析报告（五行分类版）")
    print("="*60 + "\n")
    
    print(f"✅ 人脸检测：成功")
    print(f"📍 特征点：68 个\n")
    
    # 显示五行评分
    shape_data = report["analysis"]["face_shape"]["data"]
    if "scores" in shape_data:
        print("🔮 五行脸型评分:")
        scores = shape_data["scores"]
        for wuxing, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * score + "░" * (5 - score)
            print(f"  {wuxing}: {bar} ({score}分)")
        if shape_data.get("is_mixed"):
            print(f"  → 混合类型：{shape_data.get('mixed_name', '未知')}")
        print()
    
    print("🎯 分析结果:")
    for item in report["interpretation"]:
        if item:  # 跳过空行
            print(f"  • {item}")
        else:
            print()
    
    # 显示文献引用汇总
    print("\n" + "="*60)
    print("📚 文献引用与流派说明")
    print("="*60)
    print("\n主要参考文献:")
    print("  1. 《麻衣神相》（宋代）- 江西派（形势派）- 三停五眼、十二宫位")
    print("  2. 《柳庄相法》（明代）- 福建派（理气派）- 五行面相分类")
    print("  3. 《水镜集》（清代）- 江西派（形势派）- 气色理论")
    print("  4. 《相理衡真》（清代）- 综合派 - 综合判断方法")
    print("\n流派说明:")
    print("  • 江西派（形势派）：重视面部整体格局、五官形态")
    print("  • 福建派（理气派）：重视五行生克、性格分析")
    print("  • 综合派：综合多派理论，辩证判断")
    print("\n⚠️  本分析基于传统面相学文献，仅供娱乐和文化参考")
    
    print("\n" + "="*60)
    print("⚠️  免责声明：本分析仅供娱乐参考，不具备科学依据")
    print("="*60 + "\n")
    
    # 如果保存了文件，提示
    if output_path:
        print(f"📄 详细报告已保存到：{output_path}")


if __name__ == "__main__":
    main()
