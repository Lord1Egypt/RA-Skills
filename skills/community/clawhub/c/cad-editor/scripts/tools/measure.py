"""测量工具 - 长度、面积、距离、角度"""
import math


class MeasureTool:
    """几何测量"""

    @staticmethod
    def distance(p1: tuple, p2: tuple) -> float:
        """两点间距离"""
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

    @staticmethod
    def midpoint(p1: tuple, p2: tuple) -> tuple:
        """两点中点"""
        return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

    @staticmethod
    def angle_between(p1: tuple, vertex: tuple, p2: tuple) -> float:
        """三点夹角（度）"""
        v1 = (p1[0]-vertex[0], p1[1]-vertex[1])
        v2 = (p2[0]-vertex[0], p2[1]-vertex[1])
        
        dot = v1[0]*v2[0] + v1[1]*v2[1]
        l1 = math.sqrt(v1[0]**2+v1[1]**2)
        l2 = math.sqrt(v2[0]**2+v2[1]**2)
        
        if l1 < 1e-6 or l2 < 1e-6:
            return 0.0
            
        cos_angle = max(-1, min(1, dot/(l1*l2)))
        return math.degrees(math.acos(cos_angle))

    @staticmethod
    def polygon_area(points: list) -> float:
        """
        多边形面积（Shoelace公式，逆时针为正）
        支持凸多边形和凹多边形
        """
        n = len(points)
        if n < 3:
            return 0.0
            
        area = 0.0
        for i in range(n):
            j = (i+1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
            
        return abs(area) / 2.0

    @staticmethod
    def polygon_perimeter(points: list) -> float:
        """多边形周长"""
        n = len(points)
        if n < 2:
            return 0.0
        perimeter = 0.0
        for i in range(n):
            perimeter += MeasureTool.distance(points[i], points[(i+1)%n])
        return perimeter

    @staticmethod
    def polygon_center(points: list) -> tuple:
        """多边形质心"""
        n = len(points)
        if n == 0:
            return (0, 0)
        cx = sum(p[0] for p in points) / n
        cy = sum(p[1] for p in points) / n
        return (cx, cy)

    @staticmethod
    def circle_properties(center: tuple, radius: float) -> dict:
        """圆的属性"""
        return {
            'area': math.pi * radius**2,
            'circumference': 2 * math.pi * radius,
            'diameter': radius * 2,
        }

    @staticmethod
    def bounding_box(points: list) -> dict:
        """包围盒 {min_x, min_y, max_x, max_y, width, height, center}"""
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return {
            'min_x': min_x, 'min_y': min_y,
            'max_x': max_x, 'max_y': max_y,
            'width': max_x - min_x,
            'height': max_y - min_y,
            'center': ((min_x+max_x)/2, (min_y+max_y)/2),
        }

    @staticmethod
    def slope(p1: tuple, p2: tuple) -> float:
        """斜率（度）"""
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if abs(dx) < 1e-10:
            return 90.0 if dy > 0 else -90.0
        return math.degrees(math.atan2(dy, dx))
