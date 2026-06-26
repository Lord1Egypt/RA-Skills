# Business Analyst — Code Examples

## Example 1

```typescript
// business-analyzer.ts
import { EventEmitter } from 'events';
import * as d3 from 'd3';

interface BusinessProcess {
  id: string;
  name: string;
  description: string;
  owner: string;
  department: string;
  type: ProcessType;
  maturityLevel: MaturityLevel;
  steps: ProcessStep[];
  inputs: ProcessInput[];
  outputs: ProcessOutput[];
  kpis: KPI[];
  risks: Risk[];
  opportunities: Opportunity[];
  systems: System[];
  stakeholders: Stakeholder[];
  currentState: ProcessState;
  futureState?: ProcessState;
  metrics: ProcessMetrics;
}

interface ProcessStep {
  id: string;
  name: string;
  description: string;
  type: StepType;
  owner: string;
  duration: Duration;
  cost: Cost;
  inputs: string[];
  outputs: string[];
  systems: string[];
  decisions?: Decision[];
  automationPotential: number;
  valueAdd: boolean;
  issues: Issue[];
}

interface ProcessMetrics {
  cycleTime: number;
  throughput: number;
  errorRate: number;
  cost: number;
  efficiency: number;
  effectiveness: number;
  satisfaction: number;
  compliance: number;
}

class BusinessAnalyzer extends EventEmitter {
  private processes: Map<string, BusinessProcess> = new Map();
  private workflows: Map<string, Workflow> = new Map();
  private capabilities: Map<string, Capability> = new Map();
  private valueStreams: Map<string, ValueStream> = new Map();
  private metricsEngine: MetricsEngine;

  constructor() {
    super();
    this.metricsEngine = new MetricsEngine();
  }

  async analyzeBusinessProcess(process: BusinessProcess): Promise<ProcessAnalysis> {
    // Map current state
    const currentState = await this.mapCurrentState(process);
    
    // Identify pain points
    const painPoints = this.identifyPainPoints(currentState);
    
    // Analyze bottlenecks
    const bottlenecks = this.analyzeBottlenecks(currentState);
    
    // Calculate metrics
    const metrics = await this.calculateProcessMetrics(currentState);
    
    // Identify improvement opportunities
    const opportunities = this.identifyOpportunities(currentState, painPoints, bottlenecks);
    
    // Design future state
    const futureState = this.designFutureState(currentState, opportunities);
    
    // Perform gap analysis
    const gapAnalysis = this.performGapAnalysis(currentState, futureState);
    
    // Generate recommendations
    const recommendations = this.generateRecommendations(gapAnalysis, opportunities);
    
    // Create implementation roadmap
    const roadmap = this.createRoadmap(recommendations, gapAnalysis);
    
    // Calculate ROI
    const roi = this.calculateROI(currentState, futureState, roadmap);
    
    return {
      currentState,
      futureState,
      painPoints,
      bottlenecks,
      opportunities,
      gapAnalysis,
      recommendations,
      roadmap,
      metrics,
      roi,
    };
  }

  private async mapCurrentState(process: BusinessProcess): Promise<ProcessState> {
    const state: ProcessState = {
      process: process.id,
      timestamp: new Date(),
      steps: [],
      flows: [],
      metrics: {},
      issues: [],
      risks: [],
    };
    
    // Map process steps
    for (const step of process.steps) {
      const mappedStep = await this.mapProcessStep(step);
      state.steps.push(mappedStep);
      
      // Identify flows between steps
      for (const output of step.outputs) {
        const nextStep = process.steps.find(s => s.inputs.includes(output));
        if (nextStep) {
          state.flows.push({
            from: step.id,
            to: nextStep.id,
            type: FlowType.SEQUENTIAL,
            condition: undefined,
          });
        }
      }
    }
    
    // Collect metrics
    state.metrics = await this.collectMetrics(process);
    
    // Identify issues
    state.issues = this.identifyIssues(process);
    
    // Assess risks
    state.risks = this.assessRisks(process);
    
    return state;
  }

  private identifyPainPoints(state: ProcessState): PainPoint[] {
    const painPoints: PainPoint[] = [];
    
    for (const step of state.steps) {
      // Check for manual processes that could be automated
      if (step.type === StepType.MANUAL && step.automationPotential > 0.7) {
        painPoints.push({
          id: this.generateId('PP'),
          type: PainPointType.MANUAL_PROCESS,
          stepId: step.id,
          description: `Manual process with high automation potential: ${step.name}`,
          impact: Impact.HIGH,
          frequency: step.frequency,
          cost: step.cost.total * step.frequency,
        });
      }
      
      // Check for duplicate work
      const duplicates = state.steps.filter(s => 
        s.id !== step.id && 
        this.areSimilarSteps(s, step)
      );
      
      if (duplicates.length > 0) {
        painPoints.push({
          id: this.generateId('PP'),
          type: PainPointType.DUPLICATE_WORK,
          stepId: step.id,
          description: `Duplicate work detected: ${step.name}`,
          impact: Impact.MEDIUM,
          frequency: step.frequency,
          cost: step.cost.total * duplicates.length,
        });
      }
      
      // Check for long wait times
      if (step.waitTime && step.waitTime > step.duration.average) {
        painPoints.push({
          id: this.generateId('PP'),
          type: PainPointType.WAIT_TIME,
          stepId: step.id,
          description: `Excessive wait time: ${step.waitTime}min vs ${step.duration.average}min processing`,
          impact: Impact.HIGH,
          frequency: step.frequency,
          cost: this.calculateWaitCost(step),
        });
      }
      
      // Check for high error rates
      if (step.errorRate > 0.05) {
        painPoints.push({
          id: this.generateId('PP'),
          type: PainPointType.HIGH_ERROR_RATE,
          stepId: step.id,
          description: `High error rate: ${(step.errorRate * 100).toFixed(1)}%`,
          impact: Impact.CRITICAL,
          frequency: step.frequency * step.errorRate,
          cost: this.calculateErrorCost(step),
        });
      }
    }
    
    return painPoints;
  }

  private analyzeBottlenecks(state: ProcessState): Bottleneck[] {
    const bottlenecks: Bottleneck[] = [];
    
    // Calculate throughput for each step
    const throughputs = new Map<string, number>();
    for (const step of state.steps) {
      throughputs.set(step.id, this.calculateThroughput(step));
    }
    
    // Find constraint (lowest throughput)
    const constraint = Array.from(throughputs.entries())
      .sort((a, b) => a[1] - b[1])[0];
    
    if (constraint) {
      const step = state.steps.find(s => s.id === constraint[0])!;
      bottlenecks.push({
        id: this.generateId('BN'),
        stepId: step.id,
        type: BottleneckType.CAPACITY,
        description: `Capacity constraint: ${step.name}`,
        throughput: constraint[1],
        impact: this.calculateBottleneckImpact(step, state),
        recommendations: this.generateBottleneckRecommendations(step),
      });
    }
    
    // Analyze resource bottlenecks
    const resourceUtilization = this.analyzeResourceUtilization(state);
    for (const [resource, utilization] of resourceUtilization) {
      if (utilization > 0.85) {
        bottlenecks.push({
          id: this.generateId('BN'),
          type: BottleneckType.RESOURCE,
          description: `Resource constraint: ${resource}`,
          utilization,
          impact: Impact.HIGH,
          recommendations: [
            `Add additional ${resource} resources`,
            `Cross-train staff for ${resource} tasks`,
            `Optimize ${resource} scheduling`,
          ],
        });
      }
    }
    
    // Analyze system bottlenecks
    const systemPerformance = this.analyzeSystemPerformance(state);
    for (const [system, performance] of systemPerformance) {
      if (performance.responseTime > 1000 || performance.availability < 0.99) {
        bottlenecks.push({
          id: this.generateId('BN'),
          type: BottleneckType.SYSTEM,
          description: `System constraint: ${system}`,
          performance,
          impact: Impact.HIGH,
          recommendations: [
            `Optimize ${system} performance`,
            `Scale ${system} infrastructure`,
            `Implement caching for ${system}`,
          ],
        });
      }
    }
    
    return bottlenecks;
  }

  private identifyOpportunities(
    state: ProcessState,
    painPoints: PainPoint[],
    bottlenecks: Bottleneck[]
  ): Opportunity[] {
    const opportunities: Opportunity[] = [];
    
    // Automation opportunities
    for (const step of state.steps) {
      if (step.automationPotential > 0.6) {
        opportunities.push({
          id: this.generateId('OPP'),
          type: OpportunityType.AUTOMATION,
          name: `Automate ${step.name}`,
          description: `Automate manual process to reduce time and errors`,
          stepIds: [step.id],
          benefits: {
            timeSaving: step.duration.average * 0.8,
            costSaving: step.cost.total * 0.7,
            qualityImprovement: 0.95 - step.errorRate,
          },
          effort: this.estimateAutomationEffort(step),
          priority: this.calculatePriority(step.automationPotential, step.frequency),
        });
      }
    }
    
    // Process redesign opportunities
    const redesignCandidates = this.identifyRedesignCandidates(state);
    for (const candidate of redesignCandidates) {
      opportunities.push({
        id: this.generateId('OPP'),
        type: OpportunityType.REDESIGN,
        name: `Redesign ${candidate.name}`,
        description: candidate.reason,
        stepIds: candidate.stepIds,
        benefits: candidate.benefits,
        effort: EffortLevel.HIGH,
        priority: Priority.MEDIUM,
      });
    }
    
    // Integration opportunities
    const integrationPoints = this.identifyIntegrationPoints(state);
    for (const point of integrationPoints) {
      opportunities.push({
        id: this.generateId('OPP'),
        type: OpportunityType.INTEGRATION,
        name: `Integrate ${point.system1} with ${point.system2}`,
        description: `Eliminate manual data transfer between systems`,
        benefits: {
          timeSaving: point.timeSaving,
          errorReduction: point.errorReduction,
          costSaving: point.costSaving,
        },
        effort: EffortLevel.MEDIUM,
        priority: Priority.HIGH,
      });
    }
    
    // Elimination opportunities
    for (const step of state.steps) {
      if (!step.valueAdd && step.type !== StepType.COMPLIANCE) {
        opportunities.push({
          id: this.generateId('OPP'),
          type: OpportunityType.ELIMINATION,
          name: `Eliminate ${step.name}`,
          description: `Remove non-value-adding step`,
          stepIds: [step.id],
          benefits: {
            timeSaving: step.duration.average,
            costSaving: step.cost.total,
          },
          effort: EffortLevel.LOW,
          priority: Priority.HIGH,
        });
      }
    }
    
    return opportunities;
  }

  private designFutureState(
    currentState: ProcessState,
    opportunities: Opportunity[]
  ): ProcessState {
    const futureState: ProcessState = JSON.parse(JSON.stringify(currentState));
    
    // Apply opportunities to create future state
    for (const opportunity of opportunities) {
      switch (opportunity.type) {
        case OpportunityType.AUTOMATION:
          this.applyAutomation(futureState, opportunity);
          break;
        case OpportunityType.REDESIGN:
          this.applyRedesign(futureState, opportunity);
          break;
        case OpportunityType.INTEGRATION:
          this.applyIntegration(futureState, opportunity);
          break;
        case OpportunityType.ELIMINATION:
          this.applyElimination(futureState, opportunity);
          break;
      }
    }
    
    // Recalculate metrics for future state
    futureState.metrics = this.calculateFutureMetrics(futureState, opportunities);
    
    // Optimize flow
    this.optimizeProcessFlow(futureState);
    
    return futureState;
  }

  private performGapAnalysis(
    currentState: ProcessState,
    futureState: ProcessState
  ): GapAnalysis {
    const gaps: Gap[] = [];
    
    // Process gaps
    gaps.push(...this.identifyProcessGaps(currentState, futureState));
    
    // Technology gaps
    gaps.push(...this.identifyTechnologyGaps(currentState, futureState));
    
    // People/Skills gaps
    gaps.push(...this.identifySkillGaps(currentState, futureState));
    
    // Data gaps
    gaps.push(...this.identifyDataGaps(currentState, futureState));
    
    // Calculate gap score
    const gapScore = this.calculateGapScore(gaps);
    
    return {
      gaps,
      score: gapScore,
      complexity: this.assessComplexity(gaps),
      risk: this.assessTransformationRisk(gaps),
      timeline: this.estimateTimeline(gaps),
      cost: this.estimateCost(gaps),
    };
  }

  async performCostBenefitAnalysis(
    initiative: Initiative
  ): Promise<CostBenefitAnalysis> {
    // Calculate costs
    const costs = await this.calculateCosts(initiative);
    
    // Calculate benefits
    const benefits = await this.calculateBenefits(initiative);
    
    // Financial metrics
    const npv = this.calculateNPV(costs, benefits, initiative.duration);
    const irr = this.calculateIRR(costs, benefits);
    const paybackPeriod = this.calculatePaybackPeriod(costs, benefits);
    const roi = ((benefits.total - costs.total) / costs.total) * 100;
    
    // Risk analysis
    const risks = this.analyzeInitiativeRisks(initiative);
    const riskAdjustedROI = roi * (1 - this.calculateRiskFactor(risks));
    
    // Sensitivity analysis
    const sensitivity = this.performSensitivityAnalysis(costs, benefits);
    
    return {
      costs,
      benefits,
      npv,
      irr,
      paybackPeriod,
      roi,
      riskAdjustedROI,
      risks,
      sensitivity,
      recommendation: this.generateCBARecommendation(roi, riskAdjustedROI, paybackPeriod),
    };
  }

  private calculateCosts(initiative: Initiative): Costs {
    const costs: Costs = {
      oneTime: {
        development: 0,
        implementation: 0,
        training: 0,
        infrastructure: 0,
        consulting: 0,
      },
      recurring: {
        licensing: 0,
        maintenance: 0,
        support: 0,
        operations: 0,
      },
      total: 0,
    };
    
    // Development costs
    costs.oneTime.development = this.estimateDevelopmentCost(initiative);
    
    // Implementation costs
    costs.oneTime.implementation = this.estimateImplementationCost(initiative);
    
    // Training costs
    costs.oneTime.training = this.estimateTrainingCost(initiative);
    
    // Infrastructure costs
    costs.oneTime.infrastructure = this.estimateInfrastructureCost(initiative);
    
    // Recurring costs
    costs.recurring.licensing = this.estimateLicensingCost(initiative);
    costs.recurring.maintenance = costs.oneTime.development * 0.2; // 20% of dev cost
    costs.recurring.support = this.estimateSupportCost(initiative);
    
    // Calculate total
    costs.total = Object.values(costs.oneTime).reduce((a, b) => a + b, 0) +
                  Object.values(costs.recurring).reduce((a, b) => a + b, 0) * initiative.duration;
    
    return costs;
  }

  private calculateBenefits(initiative: Initiative): Benefits {
    const benefits: Benefits = {
      tangible: {
        costSavings: 0,
        revenueIncrease: 0,
        productivityGains: 0,
        errorReduction: 0,
      },
      intangible: {
        customerSatisfaction: 0,
        employeeSatisfaction: 0,
        brandValue: 0,
        competitiveAdvantage: 0,
      },
      total: 0,
    };
    
    // Tangible benefits
    benefits.tangible.costSavings = this.calculateCostSavings(initiative);
    benefits.tangible.revenueIncrease = this.calculateRevenueIncrease(initiative);
    benefits.tangible.productivityGains = this.calculateProductivityGains(initiative);
    benefits.tangible.errorReduction = this.calculateErrorReductionValue(initiative);
    
    // Intangible benefits (assigned monetary values)
    benefits.intangible.customerSatisfaction = this.valuateCustomerSatisfaction(initiative);
    benefits.intangible.employeeSatisfaction = this.valuateEmployeeSatisfaction(initiative);
    
    // Calculate total
    benefits.total = Object.values(benefits.tangible).reduce((a, b) => a + b, 0) +
                     Object.values(benefits.intangible).reduce((a, b) => a + b, 0) * 0.5; // Weight intangibles
    
    return benefits;
  }

  private calculateNPV(costs: Costs, benefits: Benefits, years: number): number {
    const discountRate = 0.1; // 10% discount rate
    let npv = -costs.oneTime.development - costs.oneTime.implementation;
    
    for (let year = 1; year <= years; year++) {
      const annualCashFlow = (benefits.total / years) - 
                             (Object.values(costs.recurring).reduce((a, b) => a + b, 0));
      npv += annualCashFlow / Math.pow(1 + discountRate, year);
    }
    
    return npv;
  }

  async createWorkflowDesign(requirements: WorkflowRequirements): Promise<Workflow> {
    const workflow: Workflow = {
      id: this.generateId('WF'),
      name: requirements.name,
      description: requirements.description,
      trigger: requirements.trigger,
      steps: [],
      rules: [],
      integrations: [],
      notifications: [],
      sla: requirements.sla,
      metrics: [],
    };
    
    // Design workflow steps
    workflow.steps = this.designWorkflowSteps(requirements);
    
    // Define business rules
    workflow.rules = this.defineBusinessRules(requirements);
    
    // Identify integrations
    workflow.integrations = this.identifyIntegrations(requirements);
    
    // Setup notifications
    workflow.notifications = this.setupNotifications(requirements);
    
    // Define metrics
    workflow.metrics = this.defineWorkflowMetrics(requirements);
    
    // Validate workflow
    this.validateWorkflow(workflow);
    
    // Store workflow
    this.workflows.set(workflow.id, workflow);
    
    return workflow;
  }

  private designWorkflowSteps(requirements: WorkflowRequirements): WorkflowStep[] {
    const steps: WorkflowStep[] = [];
    
    // Start step
    steps.push({
      id: this.generateId('WS'),
      name: 'Start',
      type: WorkflowStepType.START,
      description: 'Workflow initiation',
      actions: [],
      transitions: [{
        to: 'step-1',
        condition: 'always',
      }],
    });
    
    // Process steps based on requirements
    for (let i = 0; i < requirements.activities.length; i++) {
      const activity = requirements.activities[i];
      
      steps.push({
        id: `step-${i + 1}`,
        name: activity.name,
        type: this.determineStepType(activity),
        description: activity.description,
        assignee: activity.assignee,
        actions: this.defineStepActions(activity),
        validations: this.defineStepValidations(activity),
        transitions: this.defineStepTransitions(activity, i, requirements.activities.length),
        sla: activity.sla,
      });
    }
    
    // End step
    steps.push({
      id: this.generateId('WS'),
      name: 'End',
      type: WorkflowStepType.END,
      description: 'Workflow completion',
      actions: [{
        type: ActionType.COMPLETE,
        description: 'Mark workflow as complete',
      }],
      transitions: [],
    });
    
    return steps;
  }

  private generateId(prefix: string): string {
    return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private areSimilarSteps(step1: any, step2: any): boolean {
    // Check if steps perform similar functions
    const similarity = this.calculateSimilarity(step1.name, step2.name);
    return similarity > 0.8 && 
           step1.type === step2.type &&
           this.arraysOverlap(step1.inputs, step2.inputs) > 0.5;
  }

  private calculateSimilarity(str1: string, str2: string): number {
    // Simple similarity calculation
    const words1 = new Set(str1.toLowerCase().split(/\s+/));
    const words2 = new Set(str2.toLowerCase().split(/\s+/));
    const intersection = new Set([...words1].filter(x => words2.has(x)));
    const union = new Set([...words1, ...words2]);
    return intersection.size / union.size;
  }

  private arraysOverlap(arr1: string[], arr2: string[]): number {
    const set1 = new Set(arr1);
    const set2 = new Set(arr2);
    const intersection = new Set([...set1].filter(x => set2.has(x)));
    return intersection.size / Math.max(set1.size, set2.size);
  }

  private calculateWaitCost(step: any): number {
    // Calculate cost of wait time
    const hourlyRate = 50; // Average hourly rate
    return (step.waitTime / 60) * hourlyRate * step.frequency;
  }

  private calculateErrorCost(step: any): number {
    // Calculate cost of errors
    const reworkCost = step.cost.total * 1.5; // Rework costs 150% of original
    return reworkCost * step.errorRate * step.frequency;
  }

  private calculateThroughput(step: any): number {
    // Calculate step throughput
    const availableTime = 480; // 8 hours in minutes
    const processingTime = step.duration.average;
    return availableTime / processingTime;
  }

  private calculateBottleneckImpact(step: any, state: ProcessState): Impact {
    // Determine impact of bottleneck
    const throughput = this.calculateThroughput(step);
    const demand = state.metrics.dailyVolume || 100;
    
    if (throughput < demand * 0.5) return Impact.CRITICAL;
    if (throughput < demand * 0.8) return Impact.HIGH;
    if (throughput < demand) return Impact.MEDIUM;
    return Impact.LOW;
  }
}

// Supporting classes and types
class MetricsEngine {
  calculateProcessMetrics(process: BusinessProcess): ProcessMetrics {
    return {
      cycleTime: this.calculateCycleTime(process),
      throughput: this.calculateProcessThroughput(process),
      errorRate: this.calculateErrorRate(process),
      cost: this.calculateProcessCost(process),
      efficiency: this.calculateEfficiency(process),
      effectiveness: this.calculateEffectiveness(process),
      satisfaction: this.calculateSatisfaction(process),
      compliance: this.calculateCompliance(process),
    };
  }

  private calculateCycleTime(process: BusinessProcess): number {
    return process.steps.reduce((total, step) => 
      total + step.duration.average + (step.waitTime || 0), 0
    );
  }

  private calculateProcessThroughput(process: BusinessProcess): number {
    const bottleneck = Math.min(...process.steps.map(s => 
      480 / s.duration.average // Daily capacity
    ));
    return bottleneck;
  }

  private calculateErrorRate(process: BusinessProcess): number {
    const totalSteps = process.steps.length;
    const totalErrors = process.steps.reduce((sum, step) => 
      sum + (step.errorRate || 0), 0
    );
    return totalErrors / totalSteps;
  }

  private calculateProcessCost(process: BusinessProcess): number {
    return process.steps.reduce((total, step) => 
      total + step.cost.total * step.frequency, 0
    );
  }

  private calculateEfficiency(process: BusinessProcess): number {
    const valueAddTime = process.steps
      .filter(s => s.valueAdd)
      .reduce((sum, s) => sum + s.duration.average, 0);
    const totalTime = this.calculateCycleTime(process);
    return valueAddTime / totalTime;
  }

  private calculateEffectiveness(process: BusinessProcess): number {
    const successRate = 1 - this.calculateErrorRate(process);
    const onTimeRate = process.metrics?.onTimeDelivery || 0.9;
    return successRate * onTimeRate;
  }

  private calculateSatisfaction(process: BusinessProcess): number {
    // Simplified satisfaction calculation
    return process.metrics?.satisfaction || 0.75;
  }

  private calculateCompliance(process: BusinessProcess): number {
    const complianceSteps = process.steps.filter(s => 
      s.type === StepType.COMPLIANCE
    );
    const compliantSteps = complianceSteps.filter(s => 
      s.complianceRate > 0.95
    );
    return complianceSteps.length > 0 
      ? compliantSteps.length / complianceSteps.length 
      : 1;
  }
}

// Type definitions
enum ProcessType {
  OPERATIONAL = 'operational',
  SUPPORT = 'support',
  MANAGEMENT = 'management',
}

enum MaturityLevel {
  INITIAL = 1,
  MANAGED = 2,
  DEFINED = 3,
  QUANTITATIVELY_MANAGED = 4,
  OPTIMIZING = 5,
}

enum StepType {
  MANUAL = 'manual',
  AUTOMATED = 'automated',
  SEMI_AUTOMATED = 'semi_automated',
  DECISION = 'decision',
  APPROVAL = 'approval',
  COMPLIANCE = 'compliance',
}

enum FlowType {
  SEQUENTIAL = 'sequential',
  PARALLEL = 'parallel',
  CONDITIONAL = 'conditional',
  LOOP = 'loop',
}

enum PainPointType {
  MANUAL_PROCESS = 'manual_process',
  DUPLICATE_WORK = 'duplicate_work',
  WAIT_TIME = 'wait_time',
  HIGH_ERROR_RATE = 'high_error_rate',
  BOTTLENECK = 'bottleneck',
  COMPLIANCE_ISSUE = 'compliance_issue',
}

enum OpportunityType {
  AUTOMATION = 'automation',
  REDESIGN = 'redesign',
  INTEGRATION = 'integration',
  ELIMINATION = 'elimination',
  OPTIMIZATION = 'optimization',
}

enum BottleneckType {
  CAPACITY = 'capacity',
  RESOURCE = 'resource',
  SYSTEM = 'system',
  APPROVAL = 'approval',
}

enum Impact {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
}

enum Priority {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
}

enum EffortLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  VERY_HIGH = 'very_high',
}

enum WorkflowStepType {
  START = 'start',
  END = 'end',
  TASK = 'task',
  DECISION = 'decision',
  PARALLEL = 'parallel',
  SUBPROCESS = 'subprocess',
}

enum ActionType {
  EXECUTE = 'execute',
  APPROVE = 'approve',
  NOTIFY = 'notify',
  COMPLETE = 'complete',
  ESCALATE = 'escalate',
}

interface ProcessInput {
  id: string;
  name: string;
  type: string;
  source: string;
  required: boolean;
}

interface ProcessOutput {
  id: string;
  name: string;
  type: string;
  destination: string;
  format: string;
}

interface KPI {
  id: string;
  name: string;
  description: string;
  formula: string;
  target: number;
  current: number;
  unit: string;
  frequency: string;
}

interface Risk {
  id: string;
  description: string;
  probability: number;
  impact: number;
  mitigation: string;
  owner: string;
}

interface Opportunity {
  id: string;
  type: OpportunityType;
  name: string;
  description: string;
  stepIds?: string[];
  benefits: any;
  effort: EffortLevel;
  priority: Priority;
}

interface System {
  id: string;
  name: string;
  type: string;
  owner: string;
  integrations: string[];
}

interface Stakeholder {
  id: string;
  name: string;
  role: string;
  department: string;
  influence: number;
  interest: number;
}

interface ProcessState {
  process: string;
  timestamp: Date;
  steps: any[];
  flows: any[];
  metrics: any;
  issues: Issue[];
  risks: Risk[];
}

interface Duration {
  min: number;
  average: number;
  max: number;
  unit: string;
}

interface Cost {
  labor: number;
  material: number;
  overhead: number;
  total: number;
}

interface Decision {
  id: string;
  question: string;
  options: string[];
  criteria: string[];
  outcome: string;
}

interface Issue {
  id: string;
  type: string;
  description: string;
  severity: string;
  frequency: number;
}

interface ProcessAnalysis {
  currentState: ProcessState;
  futureState: ProcessState;
  painPoints: PainPoint[];
  bottlenecks: Bottleneck[];
  opportunities: Opportunity[];
  gapAnalysis: GapAnalysis;
  recommendations: Recommendation[];
  roadmap: Roadmap;
  metrics: ProcessMetrics;
  roi: ROI;
}

interface PainPoint {
  id: string;
  type: PainPointType;
  stepId?: string;
  description: string;
  impact: Impact;
  frequency: number;
  cost: number;
}

interface Bottleneck {
  id: string;
  stepId?: string;
  type: BottleneckType;
  description: string;
  throughput?: number;
  utilization?: number;
  performance?: any;
  impact: Impact;
  recommendations: string[];
}

interface GapAnalysis {
  gaps: Gap[];
  score: number;
  complexity: string;
  risk: string;
  timeline: number;
  cost: number;
}

interface Gap {
  id: string;
  type: string;
  current: string;
  future: string;
  description: string;
  actions: string[];
  effort: EffortLevel;
}

interface Recommendation {
  id: string;
  title: string;
  description: string;
  priority: Priority;
  effort: EffortLevel;
  impact: Impact;
  dependencies: string[];
  risks: string[];
}

interface Roadmap {
  phases: Phase[];
  milestones: Milestone[];
  dependencies: Dependency[];
  timeline: Timeline;
  budget: Budget;
}

interface Phase {
  id: string;
  name: string;
  description: string;
  startDate: Date;
  endDate: Date;
  deliverables: string[];
  resources: Resource[];
}

interface Milestone {
  id: string;
  name: string;
  date: Date;
  criteria: string[];
  dependencies: string[];
}

interface Dependency {
  from: string;
  to: string;
  type: string;
  lag: number;
}

interface Timeline {
  start: Date;
  end: Date;
  duration: number;
  criticalPath: string[];
}

interface Budget {
  total: number;
  categories: any;
  contingency: number;
}

interface Resource {
  type: string;
  quantity: number;
  cost: number;
  availability: number;
}

interface ROI {
  investment: number;
  return: number;
  percentage: number;
  paybackPeriod: number;
  npv: number;
  irr: number;
}

interface Initiative {
  id: string;
  name: string;
  description: string;
  scope: string[];
  objectives: string[];
  duration: number;
  resources: Resource[];
}

interface CostBenefitAnalysis {
  costs: Costs;
  benefits: Benefits;
  npv: number;
  irr: number;
  paybackPeriod: number;
  roi: number;
  riskAdjustedROI: number;
  risks: Risk[];
  sensitivity: any;
  recommendation: string;
}

interface Costs {
  oneTime: any;
  recurring: any;
  total: number;
}

interface Benefits {
  tangible: any;
  intangible: any;
  total: number;
}

interface Workflow {
  id: string;
  name: string;
  description: string;
  trigger: any;
  steps: WorkflowStep[];
  rules: BusinessRule[];
  integrations: Integration[];
  notifications: Notification[];
  sla: SLA;
  metrics: Metric[];
}

interface WorkflowStep {
  id: string;
  name: string;
  type: WorkflowStepType;
  description: string;
  assignee?: string;
  actions: Action[];
  validations?: Validation[];
  transitions: Transition[];
  sla?: SLA;
}

interface BusinessRule {
  id: string;
  name: string;
  condition: string;
  action: string;
  priority: number;
}

interface Integration {
  id: string;
  system: string;
  type: string;
  endpoint: string;
  authentication: string;
}

interface Notification {
  id: string;
  trigger: string;
  recipients: string[];
  template: string;
  channel: string;
}

interface SLA {
  responseTime: number;
  resolutionTime: number;
  availability: number;
  escalation: string[];
}

interface Metric {
  id: string;
  name: string;
  formula: string;
  threshold: number;
  frequency: string;
}

interface Action {
  type: ActionType;
  description: string;
  parameters?: any;
}

interface Validation {
  field: string;
  rule: string;
  message: string;
}

interface Transition {
  to: string;
  condition: string;
  priority?: number;
}

interface WorkflowRequirements {
  name: string;
  description: string;
  trigger: any;
  activities: Activity[];
  sla: SLA;
  stakeholders: string[];
}

interface Activity {
  name: string;
  description: string;
  type: string;
  assignee: string;
  inputs: string[];
  outputs: string[];
  sla?: SLA;
}

interface Capability {
  id: string;
  name: string;
  description: string;
  maturity: MaturityLevel;
  processes: string[];
  systems: string[];
  metrics: Metric[];
}

interface ValueStream {
  id: string;
  name: string;
  customer: string;
  value: string;
  steps: string[];
  metrics: any;
}

// Export the analyzer
export { BusinessAnalyzer, BusinessProcess, ProcessAnalysis };
```
