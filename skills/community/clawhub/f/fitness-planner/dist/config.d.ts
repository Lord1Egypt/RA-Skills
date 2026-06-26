import { Config, UserConfig, Gender, Goal, Location, Experience } from './types.js';
/**
 * 加载配置
 */
export declare function loadConfig(): Config;
/**
 * 保存配置
 */
export declare function saveConfig(config: Config): void;
/**
 * 检查配置是否完整
 */
export declare function isConfigComplete(config: Config): boolean;
/**
 * 更新用户配置
 */
export declare function updateUserConfig(updates: Partial<UserConfig>): Config;
/**
 * 获取缺失的配置项
 */
export declare function getMissingFields(config: Config): string[];
/**
 * 解析用户输入
 */
export declare function parseGender(input: string): Gender | null;
export declare function parseGoal(input: string): Goal | null;
export declare function parseLocation(input: string): Location | null;
export declare function parseExperience(input: string): Experience | null;
export declare function parseNumber(input: string): number | null;
