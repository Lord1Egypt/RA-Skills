#!/usr/bin/env python3
"""
代码生成模块
负责生成高质量的代码
"""

import os
import json
import logging
from datetime import datetime
from .model_manager import ModelManager

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self):
        self.model_manager = ModelManager()
        self.language_templates = {
            'python': {
                'hello_world': '''
# Python Hello World
print("Hello, World!")
''',
                'web_server': '''
# Python Web Server using Flask
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
''',
                'data_analysis': '''
# Python Data Analysis using pandas
import pandas as pd

# Read data
df = pd.read_csv('data.csv')

# Basic analysis
print(df.head())
print(df.describe())

# Filter data
filtered = df[df['value'] > 100]
print(filtered)
'''
            },
            'javascript': {
                'hello_world': '''
// JavaScript Hello World
console.log("Hello, World!");
''',
                'web_server': '''
// JavaScript Web Server using Express
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
''',
                'react_component': '''
// React Component
import React from 'react';

function HelloWorld() {
  return (
    <div>
      <h1>Hello, World!</h1>
      <p>Welcome to React</p>
    </div>
  );
}

export default HelloWorld;
'''
            },
            'go': {
                'hello_world': '''
// Go Hello World
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
''',
                'web_server': '''
// Go Web Server
package main

import (
    "fmt"
    "net/http"
)

func hello(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, World!")
}

func main() {
    http.HandleFunc("/", hello)
    http.ListenAndServe(":8080", nil)
}
'''
            },
            'java': {
                'hello_world': '''
// Java Hello World
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
''',
                'web_server': '''
// Java Web Server using Spring Boot
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class Application {

    @GetMapping("/")
    public String hello() {
        return "Hello, World!";
    }

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
'''
            }
        }
        self.code_templates = {
            'function': '''
请生成一个{language}函数，实现以下功能：
{function_description}

要求：
1. 函数名合理
2. 参数类型明确
3. 包含适当的注释
4. 处理边界情况
5. 代码风格符合{language}标准
''',
            'class': '''
请生成一个{language}类，实现以下功能：
{class_description}

要求：
1. 类名合理
2. 包含必要的属性和方法
3. 构造函数完整
4. 包含适当的注释
5. 代码风格符合{language}标准
''',
            'module': '''
请生成一个{language}模块，实现以下功能：
{module_description}

要求：
1. 模块结构清晰
2. 包含必要的函数和类
3. 提供适当的文档
4. 处理错误情况
5. 代码风格符合{language}标准
''',
            'algorithm': '''
请生成一个{language}实现，实现以下算法：
{algorithm_description}

要求：
1. 算法实现正确
2. 时间复杂度合理
3. 包含适当的注释
4. 提供测试用例
5. 代码风格符合{language}标准
'''
        }
    
    def generate(self, prompt, model_name='default', max_tokens=2000):
        """生成代码
        
        Args:
            prompt: 提示词
            model_name: 模型名称
            max_tokens: 最大 token 数
            
        Returns:
            result: 生成结果
        """
        return self.model_manager.generate(prompt, model_name, max_tokens)
    
    def generate_from_template(self, template_name, template_vars, model_name='default', max_tokens=2000):
        """使用模板生成代码
        
        Args:
            template_name: 模板名称
            template_vars: 模板变量
            model_name: 模型名称
            max_tokens: 最大 token 数
            
        Returns:
            result: 生成结果
        """
        if template_name not in self.code_templates:
            logger.error(f"模板不存在: {template_name}")
            return "模板不存在"
        
        try:
            # 填充模板
            prompt = self.code_templates[template_name].format(**template_vars)
            # 生成代码
            result = self.generate(prompt, model_name, max_tokens)
            return result
        except Exception as e:
            logger.error(f"生成失败: {str(e)}")
            return f"生成失败: {str(e)}"
    
    def generate_function(self, language, function_description, model_name='default'):
        """生成函数
        
        Args:
            language: 编程语言
            function_description: 函数描述
            model_name: 模型名称
            
        Returns:
            code: 生成的函数代码
        """
        return self.generate_from_template(
            'function',
            {
                'language': language,
                'function_description': function_description
            },
            model_name
        )
    
    def generate_class(self, language, class_description, model_name='default'):
        """生成类
        
        Args:
            language: 编程语言
            class_description: 类描述
            model_name: 模型名称
            
        Returns:
            code: 生成的类代码
        """
        return self.generate_from_template(
            'class',
            {
                'language': language,
                'class_description': class_description
            },
            model_name
        )
    
    def generate_module(self, language, module_description, model_name='default'):
        """生成模块
        
        Args:
            language: 编程语言
            module_description: 模块描述
            model_name: 模型名称
            
        Returns:
            code: 生成的模块代码
        """
        return self.generate_from_template(
            'module',
            {
                'language': language,
                'module_description': module_description
            },
            model_name
        )
    
    def generate_algorithm(self, language, algorithm_description, model_name='default'):
        """生成算法实现
        
        Args:
            language: 编程语言
            algorithm_description: 算法描述
            model_name: 模型名称
            
        Returns:
            code: 生成的算法代码
        """
        return self.generate_from_template(
            'algorithm',
            {
                'language': language,
                'algorithm_description': algorithm_description
            },
            model_name
        )
    
    def generate_from_language_template(self, language, template_name):
        """从语言模板生成代码
        
        Args:
            language: 编程语言
            template_name: 模板名称
            
        Returns:
            code: 生成的代码
        """
        if language not in self.language_templates:
            logger.error(f"不支持的语言: {language}")
            return "不支持的语言"
        
        if template_name not in self.language_templates[language]:
            logger.error(f"模板不存在: {template_name}")
            return "模板不存在"
        
        return self.language_templates[language][template_name]
    
    def add_language_template(self, language, template_name, template_content):
        """添加语言模板
        
        Args:
            language: 编程语言
            template_name: 模板名称
            template_content: 模板内容
        """
        if language not in self.language_templates:
            self.language_templates[language] = {}
        
        self.language_templates[language][template_name] = template_content
        logger.info(f"添加语言模板成功: {language}/{template_name}")
    
    def remove_language_template(self, language, template_name):
        """删除语言模板
        
        Args:
            language: 编程语言
            template_name: 模板名称
        """
        if language in self.language_templates and template_name in self.language_templates[language]:
            del self.language_templates[language][template_name]
            logger.info(f"删除语言模板成功: {language}/{template_name}")
        else:
            logger.warning(f"模板不存在: {language}/{template_name}")
    
    def list_language_templates(self, language=None):
        """列出语言模板
        
        Args:
            language: 编程语言
            
        Returns:
            templates: 模板列表
        """
        if language:
            return list(self.language_templates.get(language, {}).keys())
        else:
            return {
                lang: list(templates.keys()) 
                for lang, templates in self.language_templates.items()
            }
    
    def list_supported_languages(self):
        """列出支持的语言
        
        Returns:
            languages: 语言列表
        """
        return list(self.language_templates.keys())

if __name__ == "__main__":
    # 测试代码生成器
    generator = CodeGenerator()
    
    # 测试语言模板
    print("测试语言模板 - Python Hello World:")
    result = generator.generate_from_language_template('python', 'hello_world')
    print(result)
    print()
    
    # 测试函数生成
    print("测试函数生成 - Python 阶乘函数:")
    result = generator.generate_function('python', '计算阶乘')
    print(result)
    print()
    
    # 测试类生成
    print("测试类生成 - Python 学生类:")
    result = generator.generate_class('python', '学生类，包含姓名、年龄和成绩属性，以及计算平均成绩的方法')
    print(result)
    print()
    
    # 测试模块生成
    print("测试模块生成 - Python 数学工具模块:")
    result = generator.generate_module('python', '数学工具模块，包含常用的数学函数如求和、平均值、标准差等')
    print(result)
    print()
    
    # 测试算法生成
    print("测试算法生成 - Python 二分查找:")
    result = generator.generate_algorithm('python', '二分查找算法，在有序数组中查找目标值')
    print(result)
