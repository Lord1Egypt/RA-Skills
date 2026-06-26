# calculus-intelligent-grading - 高等数学多模态智能批改Skill

## 概述
专门针对高等数学主观题的智能批改系统，支持LaTeX公式验证、推导过程检查、多模态批注生成。整合OCR识别、符号计算和LLM分析，实现AI助教+人工复核双模式批改。

## 核心功能

### 1. 多模态输入支持
- **图像识别**: 手写数学公式OCR识别
- **LaTeX解析**: 符号公式语义分析
- **步骤分割**: 自动分割解题步骤
- **结构理解**: 理解证明逻辑结构

### 2. 智能批改引擎
- **符号计算验证**: 使用SymPy验证数学计算
- **步骤依赖分析**: 检查推导逻辑完整性
- **错误类型分类**: 概念错误/计算错误/逻辑跳跃
- **部分得分计算**: 根据正确步骤给予部分分数

### 3. 多模态反馈生成
- **文字批注**: 精准定位错误位置
- **语音讲解**: TTS生成知识点讲解
- **视频推荐**: 关联教学视频资源
- **可视化对比**: 展示正确解法动画

## 工具定义

### grade_submission
批改学生作业提交

**参数**：
- `submission_type` (string): 提交类型，"image"、"latex"、"text"
- `submission_content` (string): 提交内容（Base64图像或文本）
- `reference_answer` (string): 标准答案（LaTeX格式）
- `grading_mode` (string): 批改模式，"auto"、"assisted"、"manual"
- `detailed_feedback` (boolean): 是否生成详细反馈

**返回**：
```json
{
  "submission_id": "sub_001",
  "overall_score": 85,
  "step_scores": [
    {
      "step_no": 1,
      "is_correct": true,
      "score": 20,
      "content": "设f(x)=x²"
    },
    {
      "step_no": 2, 
      "is_correct": false,
      "score": 10,
      "error_type": "calculation_error",
      "error_detail": "积分计算错误",
      "suggestion": "应为∫x² dx = x³/3 + C"
    }
  ],
  "feedback": {
    "text_annotations": [
      {
        "position": "step2",
        "type": "error",
        "content": "积分公式应用错误"
      }
    ],
    "voice_feedback": "data:audio/mp3;base64,...",
    "recommended_videos": [
      {
        "title": "定积分计算方法",
        "url": "https://example.com/video1"
      }
    ]
  }
}
```

### analyze_proof_structure
分析证明题逻辑结构

**参数**：
- `proof_text` (string): 证明过程文本
- `theorem_statement` (string): 定理陈述
- `check_logical_jumps` (boolean): 检查逻辑跳跃

**返回**：
```json
{
  "proof_id": "proof_001",
  "structure_valid": true,
  "logical_steps": [
    {
      "step": 1,
      "type": "assumption",
      "content": "假设f在[a,b]连续",
      "valid": true
    },
    {
      "step": 2,
      "type": "application",
      "content": "应用中值定理",
      "valid": true,
      "theorem_used": "Lagrange中值定理"
    },
    {
      "step": 3,
      "type": "conclusion",
      "content": "因此存在ξ∈(a,b)",
      "valid": true,
      "depends_on": [1, 2]
    }
  ],
  "logical_jumps": [],
  "completeness_score": 95
}
```

### generate_multimodal_feedback
生成多模态批注反馈

**参数**：
- `error_analysis` (object): 错误分析结果
- `student_level` (string): 学生水平
- `feedback_mode` (string): 反馈模式，"text"、"voice"、"mixed"

**返回**：
```json
{
  "feedback_id": "fb_001",
  "modes": {
    "text": [
      {
        "annotation": "第2步积分计算错误",
        "correct_form": "∫x² dx = x³/3 + C",
        "explanation": "幂函数积分公式：∫xⁿ dx = xⁿ⁺¹/(n+1) + C"
      }
    ],
    "voice": {
      "url": "data:audio/mp3;base64,...",
      "duration": 30,
      "topics": ["积分基本公式"]
    },
    "visual": {
      "animation_url": "https://geogebra.org/...",
      "type": "integral_calculation"
    }
  },
  "personalized": true
}
```

## 使用示例

### 示例1：批改图像作业
```bash
# 批改手写作业图像
openclaw skill calculus-intelligent-grading grade_submission \
  --submission-type "image" \
  --submission-content "$(base64 student_work.jpg)" \
  --reference-answer "\\int_0^1 x^2 dx = \\frac{1}{3}" \
  --grading-mode "auto" \
  --detailed-feedback true
```

### 示例2：分析证明题
```bash
# 分析证明题逻辑结构
openclaw skill calculus-intelligent-grading analyze_proof_structure \
  --proof-text "假设f在[a,b]连续...应用中值定理..." \
  --theorem-statement "罗尔定理" \
  --check-logical-jumps true
```

### 示例3：生成语音批注
```bash
# 为错误步骤生成语音讲解
openclaw skill calculus-intelligent-grading generate_multimodal_feedback \
  --error-analysis '{"step":2,"error_type":"concept_error","topic":"积分"}' \
  --student-level "中等" \
  --feedback-mode "mixed"
```

## 技术实现

### 核心批改引擎
```python
class CalculusGradingEngine:
    def __init__(self):
        self.ocr = MathOCR()          # 数学公式OCR
        self.sympy = SymPyValidator() # 符号计算验证
        self.llm = LLMGrader()        # LLM语义分析
        self.validator = StepValidator() # 步骤验证
        
    async def grade(self, submission, reference):
        # 1. 内容识别
        if submission.type == "image":
            content = await self.ocr.recognize(submission.image)
        else:
            content = submission.content
            
        # 2. 步骤分割
        steps = self.segment_steps(content)
        
        # 3. 逐步骤批改
        results = []
        for i, step in enumerate(steps):
            result = await self.grade_step(step, reference, i)
            results.append(result)
            
        # 4. 生成反馈
        feedback = self.generate_feedback(results)
        
        return GradingResult(
            score=self.calculate_score(results),
            step_results=results,
            feedback=feedback
        )
```

### 符号计算验证
```python
class SymPyValidator:
    def validate_integral(self, student_expr, correct_expr, variable='x'):
        """验证积分计算"""
        try:
            # 解析表达式
            student_sympy = parse_expr(student_expr)
            correct_sympy = parse_expr(correct_expr)
            
            # 计算导数验证
            student_derivative = diff(student_sympy, variable)
            correct_derivative = diff(correct_sympy, variable)
            
            # 符号等价性检查
            return simplify(student_derivative - correct_derivative) == 0
            
        except Exception as e:
            return False, f"表达式解析错误: {str(e)}"
```

### LLM语义分析
```python
class LLMGrader:
    def __init__(self, model="deepseek/deepseek-chat"):
        self.model = model
        
    async def analyze_concept_error(self, step_content, topic):
        """分析概念性错误"""
        prompt = f"""
        分析以下高等数学解题步骤中的概念错误：
        知识点：{topic}
        学生解答：{step_content}
        
        请分析：
        1. 是否存在概念理解错误
        2. 错误的具体类型
        3. 正确的概念应该是什么
        4. 如何讲解这个知识点
        """
        
        response = await self.llm_complete(prompt)
        return self.parse_analysis(response)
```

## 与现有Skill集成

### 调用calculus-concept-visualizer
```python
# 为错误生成可视化解释
from calculus_concept_visualizer import create_error_visualization

visualization = create_error_visualization(
    error_type="integral_concept",
    student_misunderstanding="认为∫x² dx = x²/2",
    correct_concept="∫xⁿ dx = xⁿ⁺¹/(n+1) + C"
)
```

### 集成calculus-error-analyzer
```python
# 深度错误分析
from calculus_error_analyzer import analyze_error_pattern

pattern = analyze_error_pattern(
    student_id="stu001",
    error_history=grading_results,
    knowledge_graph=True
)
```

## 配置说明

### 批改规则配置
```yaml
grading_rules:
  step_scoring:
    correct_step: 10
    partial_correct: 5
    concept_error: 0
    calculation_error: 2
    
  error_classification:
    concept_errors:
      - "公式记错"
      - "定理误用"
      - "定义混淆"
      
    calculation_errors:
      - "符号错误"
      - "计算失误" 
      - "化简错误"
      
    logical_errors:
      - "循环论证"
      - "逻辑跳跃"
      - "前提错误"
```

### OCR配置
```yaml
ocr_settings:
  math_formula:
    engine: "mathpix"
    confidence_threshold: 0.8
    retry_count: 3
    
  handwriting:
    engine: "google_vision"
    language: "zh"
    math_mode: true
```

## 性能优化

### 批改缓存
```python
class GradingCache:
    def __init__(self):
        self.redis = RedisCache()
        self.memory_cache = LRUCache(maxsize=1000)
        
    async def get_cached_result(self, submission_hash):
        """获取缓存批改结果"""
        # 1. 检查内存缓存
        if result := self.memory_cache.get(submission_hash):
            return result
            
        # 2. 检查Redis缓存
        if result := await self.redis.get(f"grading:{submission_hash}"):
            self.memory_cache[submission_hash] = result
            return result
            
        return None
```

### 批量处理
```python
async def batch_grade(self, submissions, parallel=4):
    """批量批改作业"""
    semaphore = asyncio.Semaphore(parallel)
    
    async def grade_one(submission):
        async with semaphore:
            return await self.grade(submission)
    
    tasks = [grade_one(sub) for sub in submissions]
    return await asyncio.gather(*tasks)
```

## 测试用例

### 单元测试
```python
def test_integral_validation():
    validator = SymPyValidator()
    
    # 测试正确积分
    valid, msg = validator.validate_integral(
        "x**3/3", 
        "x**3/3"
    )
    assert valid == True
    
    # 测试错误积分
    valid, msg = validator.validate_integral(
        "x**2/2",  # 错误
        "x**3/3"   # 正确
    )
    assert valid == False
```

### 集成测试
```python
async def test_full_grading_pipeline():
    engine = CalculusGradingEngine()
    
    # 模拟学生作业
    submission = HomeworkSubmission(
        type="latex",
        content="\\int x^2 dx = \\frac{x^2}{2} + C"  # 错误
    )
    
    reference = "\\int x^2 dx = \\frac{x^3}{3} + C"  # 正确
    
    result = await engine.grade(submission, reference)
    
    assert result.score < 50  # 应得低分
    assert "积分公式错误" in result.feedback.text_annotations[0]
```

## 部署说明

### 系统要求
- Python 3.9+
- SymPy 1.12+
- LaTeX环境（用于公式渲染）
- GPU（可选，加速LLM推理）

### 安装步骤
```bash
# 1. 安装依赖
pip install sympy opencv-python pillow
pip install torch transformers  # LLM支持

# 2. 配置OCR服务
# 需要Mathpix或Google Vision API密钥

# 3. 启动批改服务
python grading_service.py --port 8080 --workers 4
```

## 版本历史
- v1.0.0 (2026-04-16): 初始版本
  - 多模态作业批改
  - 符号计算验证
  - 步骤逻辑分析
  - 多模态反馈生成

## 作者
代国兴 - 高等数学智慧课程系统

## 许可证
MIT License