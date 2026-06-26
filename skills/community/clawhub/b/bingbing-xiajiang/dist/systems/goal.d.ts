/**
 * 个人目标追踪系统
 */
import { UnifiedMemorySystem } from '../core/memory';
type MotivationLevel = 'safety' | 'social' | 'esteem' | 'self-actualization' | 'meaning';
export interface Motivation {
    level: MotivationLevel;
    description: string;
    strength: 'high' | 'medium' | 'low';
}
export interface Goal {
    name: string;
    description: string;
    priority: number;
    progress: number;
    deadline: Date;
    motivations: Motivation[];
}
export interface EnergyAllocation {
    dimension: string;
    actualHours: number;
    actualPercentage: number;
    idealPercentage: number;
    gap: number;
}
export interface AIMirrorLetter {
    observations: string;
    progress: string[];
    concerns: {
        observation: string;
        concern: string;
        suggestion: string;
    }[];
    challenges: string[];
    possibilities: string[];
    recommendations: string[];
    closing: string;
}
export declare class PersonalGoalSystem {
    private memory;
    private systemName;
    constructor(memory: UnifiedMemorySystem);
    analyzeMotivation(goal: Goal, userResponses: Record<MotivationLevel, string>): Motivation[];
    buildGoalNetwork(goals: Goal[]): {
        goals: Goal[];
        relations: {
            goalA: string;
            goalB: string;
            relation: string;
            reason: string;
        }[];
    };
    analyzeEnergyAllocation(timeLog: Record<string, number>, idealAllocation: Record<string, number>): EnergyAllocation[];
    discoverBlindSpots(goals: Goal[], energyAllocation: EnergyAllocation[], statedPriorities: Record<string, number>): {
        type: string;
        description: string;
        impact: string;
        suggestion: string;
    }[];
    generateAIMirrorLetter(observations: string, progress: string[], concerns: {
        observation: string;
        concern: string;
        suggestion: string;
    }[], challenges: string[], possibilities: string[], recommendations: string[]): AIMirrorLetter;
    predictFutureSelf(goals: Goal[], energyAllocation: EnergyAllocation[], behaviorPatterns: string[]): {
        timeframe: string;
        capabilityState: string;
        energyState: string;
        goalProgress: string;
        lifeTrajectory?: string;
    }[];
    generateWeeklySelfAwarenessReport(period: string, goals: Goal[], timeLog: Record<string, number>, idealAllocation: Record<string, number>, statedPriorities: Record<string, number>): {
        period: string;
        keywords: string[];
        stateScores: {
            overall: number;
            energy: number;
            emotion: number;
            progress: number;
        };
        energyAllocation: EnergyAllocation[];
        goalProgress: {
            goal: string;
            weeklyProgress: number;
            totalProgress: number;
        }[];
        blindSpots: {
            type: string;
            description: string;
            impact: string;
            suggestion: string;
        }[];
        mirrorFeedback: AIMirrorLetter;
        nextWeekSuggestions: string[];
    };
    syncToOtherSystems(): void;
}
export {};
//# sourceMappingURL=goal.d.ts.map