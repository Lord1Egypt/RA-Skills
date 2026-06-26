/**
 * 意图识别引擎
 * Intent Recognition Engine
 * 基于规则 + 模式匹配的轻量级NLP
 */
import { IntentResult, QueryCondition } from '../types';
export declare class IntentEngine {
    private patterns;
    constructor();
    /**
     * 初始化识别模式
     * 注意：按优先级排序，更具体的模式在前
     */
    private initializePatterns;
    /**
     * 解析用户输入
     */
    parse(input: string): IntentResult;
    /**
     * 提取实体
     */
    private extractEntities;
    /**
     * 清理表名，移除"表"、"表格"等后缀
     */
    private cleanTableName;
    /**
     * 从文本中提取条件
     */
    private extractConditions;
    /**
     * 从文本中提取数据字段
     */
    private extractDataFields;
    /**
     * 解析值类型
     */
    private parseValue;
    /**
     * 提取报表类型
     */
    private extractReportType;
    /**
     * 计算置信度
     */
    private calculateConfidence;
    /**
     * 将条件转换为飞书filter表达式
     */
    buildFilterExpression(conditions: QueryCondition[]): string;
}
//# sourceMappingURL=intent-engine.d.ts.map