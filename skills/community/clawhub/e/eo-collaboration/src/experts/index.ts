// ============================================================================
// EO Expert Registry - 141 Experts (Core Subset for Plugin)
// ============================================================================

import type { Expert } from '../types/index.js';

// ---------------------------------------------------------------------------
// Expert Categories
// ---------------------------------------------------------------------------

export const EXPERT_CATEGORIES = {
  MANAGEMENT: 'management',
  ENGINEERING: 'engineering',
  DESIGN: 'design',
  QA: 'qa',
  DEVOPS: 'devops',
  DOMAIN: 'domain',
  SECURITY: 'security',
  DATA: 'data',
} as const;

// ---------------------------------------------------------------------------
// Core Expert Registry
// ---------------------------------------------------------------------------

export const EXPERT_REGISTRY: Record<string, Expert> = {
  // --- Management ---
  'pm': {
    id: 'pm',
    name: 'Project Manager',
    role: 'Project Manager',
    description: 'Breaks down tasks, defines sprints, tracks milestones, manages stakeholders.',
    capabilities: ['project-planning', 'requirement-analysis', 'risk-management', 'stakeholder-communication'],
    tools: ['task-board', 'gantt-chart', 'status-report'],
  },
  'product-manager': {
    id: 'product-manager',
    name: 'Product Manager',
    role: 'Product Manager',
    description: 'Defines product vision, prioritizes features, analyzes market fit.',
    capabilities: ['roadmap-planning', 'user-story-creation', 'market-analysis', 'feature-prioritization'],
    tools: ['roadmap', 'user-story', 'prd'],
  },
  'tech-lead': {
    id: 'tech-lead',
    name: 'Tech Lead',
    role: 'Technical Lead',
    description: 'Architectural decisions, code review, technical mentorship, standards.',
    capabilities: ['system-design', 'code-review', 'technical-planning', 'team-leadership'],
    tools: ['architecture-diagram', 'code-review', 'adr'],
  },
  'scrum-master': {
    id: 'scrum-master',
    name: 'Scrum Master',
    role: 'Scrum Master',
    description: 'Facilitates agile ceremonies, removes impediments, coaches teams.',
    capabilities: ['sprint-planning', 'retrospective-facilitation', 'impediment-removal', 'agile-coaching'],
    tools: ['sprint-board', 'retrospective', 'velocity-chart'],
  },

  // --- Engineering ---
  'engineer': {
    id: 'engineer',
    name: 'Software Engineer',
    role: 'Software Engineer',
    description: 'Implements features, writes tests, refactors code, fixes bugs.',
    capabilities: ['coding', 'testing', 'debugging', 'refactoring', 'code-review'],
    tools: ['ide', 'git', 'debugger', 'profiler'],
  },
  'frontend-dev': {
    id: 'frontend-dev',
    name: 'Frontend Developer',
    role: 'Frontend Developer',
    description: 'React, Vue, CSS, responsive design, accessibility, performance.',
    capabilities: ['react', 'vue', 'css', 'accessibility', 'responsive-design', 'web-performance'],
    tools: ['browser-devtools', 'lighthouse', 'storybook'],
  },
  'backend-dev': {
    id: 'backend-dev',
    name: 'Backend Developer',
    role: 'Backend Developer',
    description: 'APIs, databases, authentication, caching, message queues.',
    capabilities: ['api-design', 'database-design', 'auth', 'caching', 'microservices'],
    tools: ['postman', 'swagger', 'database-tools'],
  },
  'fullstack-dev': {
    id: 'fullstack-dev',
    name: 'Full-Stack Developer',
    role: 'Full-Stack Developer',
    description: 'Both frontend and backend development across the stack.',
    capabilities: ['frontend', 'backend', 'devops', 'database', 'api-design'],
    tools: ['ide', 'git', 'docker'],
  },
  'devops': {
    id: 'devops',
    name: 'DevOps Engineer',
    role: 'DevOps Engineer',
    description: 'CI/CD pipelines, containerization, cloud infrastructure, monitoring.',
    capabilities: ['ci-cd', 'kubernetes', 'docker', 'aws', 'gcp', 'monitoring', 'infrastructure-as-code'],
    tools: ['jenkins', 'github-actions', 'terraform', 'prometheus', 'grafana'],
  },
  'data-engineer': {
    id: 'data-engineer',
    name: 'Data Engineer',
    role: 'Data Engineer',
    description: 'ETL pipelines, data warehousing, streaming, data quality.',
    capabilities: ['etl', 'data-warehousing', 'spark', 'airflow', 'kafka', 'data-quality'],
    tools: ['spark', 'airflow', 'dbt', 'snowflake'],
  },
  'ml-engineer': {
    id: 'ml-engineer',
    name: 'ML Engineer',
    role: 'ML Engineer',
    description: 'Machine learning model training, deployment, MLOps.',
    capabilities: ['model-training', 'model-deployment', 'feature-engineering', 'mlops', 'model-monitoring'],
    tools: ['mlflow', 'kubeflow', 'tensorboard', 'WeightsAndBiases'],
  },
  'security-engineer': {
    id: 'security-engineer',
    name: 'Security Engineer',
    role: 'Security Engineer',
    description: 'Security audits, penetration testing, vulnerability assessment.',
    capabilities: ['penetration-testing', 'vulnerability-assessment', 'secure-coding', 'threat-modeling'],
    tools: ['owasp-zap', 'nmap', 'burp-suite', 'sonarqube'],
  },
  'mobile-dev': {
    id: 'mobile-dev',
    name: 'Mobile Developer',
    role: 'Mobile Developer',
    description: 'iOS, Android, React Native, Flutter app development.',
    capabilities: ['ios', 'android', 'react-native', 'flutter', 'app-store'],
    tools: ['xcode', 'android-studio', 'fastlane'],
  },

  // --- QA ---
  'qa': {
    id: 'qa',
    name: 'QA Engineer',
    role: 'QA Engineer',
    description: 'Test planning, test case design, test automation, bug reporting.',
    capabilities: ['test-planning', 'test-case-design', 'test-automation', 'bug-reporting', 'regression-testing'],
    tools: ['selenium', 'cypress', 'playwright', 'jira', 'testrail'],
  },
  'tester': {
    id: 'tester',
    name: 'Tester',
    role: 'Tester',
    description: 'Manual and automated testing, regression, performance testing.',
    capabilities: ['manual-testing', 'automated-testing', 'performance-testing', 'api-testing'],
    tools: ['postman', 'jmeter', 'katalon'],
  },
  'sdet': {
    id: 'sdet',
    name: 'SDET',
    role: 'Software Development Engineer in Test',
    description: 'Test automation framework development, test infrastructure.',
    capabilities: ['test-framework-design', 'ci-cd-testing', 'api-testing', 'performance-testing', 'test-infrastructure'],
    tools: ['selenium', 'cypress', 'playwright', 'docker'],
  },

  // --- Design ---
  'ux-researcher': {
    id: 'ux-researcher',
    name: 'UX Researcher',
    role: 'UX Researcher',
    description: 'User interviews, usability testing, personas, journey mapping.',
    capabilities: ['user-interviews', 'usability-testing', 'persona-creation', 'journey-mapping'],
    tools: ['figma', 'maze', 'userTesting'],
  },
  'ui-designer': {
    id: 'ui-designer',
    name: 'UI Designer',
    role: 'UI Designer',
    description: 'Visual design, design systems, prototyping, accessibility.',
    capabilities: ['visual-design', 'design-systems', 'prototyping', 'accessibility', 'responsive-design'],
    tools: ['figma', 'sketch', 'adobe-xd'],
  },
  'ux-designer': {
    id: 'ux-designer',
    name: 'UX Designer',
    role: 'UX Designer',
    description: 'Interaction design, information architecture, wireframing.',
    capabilities: ['interaction-design', 'information-architecture', 'wireframing', 'prototyping'],
    tools: ['figma', 'axure', 'balsamiq'],
  },

  // --- Domain Experts ---
  'dba': {
    id: 'dba',
    name: 'Database Administrator',
    role: 'DBA',
    description: 'Database design, query optimization, backup/recovery, replication.',
    capabilities: ['database-design', 'query-optimization', 'backup-recovery', 'replication', 'sharding'],
    tools: ['pgadmin', 'mysql-workbench', 'mongosh'],
  },
  'architect': {
    id: 'architect',
    name: 'Solutions Architect',
    role: 'Solutions Architect',
    description: 'System architecture, technology selection, infrastructure design.',
    capabilities: ['system-architecture', 'technology-selection', 'infrastructure-design', 'cost-optimization'],
    tools: ['draw.io', 'archimate', 'aws-diagrams'],
  },
  'api-designer': {
    id: 'api-designer',
    name: 'API Designer',
    role: 'API Designer',
    description: 'REST/GraphQL API design, versioning, documentation, OpenAPI specs.',
    capabilities: ['rest-api', 'graphql-api', 'api-versioning', 'openapi', 'api-documentation'],
    tools: ['swagger', 'postman', 'stoplight'],
  },

  // --- Code Review ---
  'code-reviewer': {
    id: 'code-reviewer',
    name: 'Code Reviewer',
    role: 'Code Reviewer',
    description: 'Code quality assessment, best practices, security vulnerabilities.',
    capabilities: ['code-quality', 'security-review', 'performance-review', 'readability-review'],
    tools: ['sonarqube', 'snyk', 'eslint', 'prettier'],
  },
  'senior-dev': {
    id: 'senior-dev',
    name: 'Senior Developer',
    role: 'Senior Developer',
    description: 'Senior-level code review, design patterns, architectural guidance.',
    capabilities: ['advanced-coding', 'design-patterns', 'code-review', 'mentoring'],
    tools: ['git', 'github', 'sonarqube'],
  },

  // --- Deployment & Operations ---
  'sre': {
    id: 'sre',
    name: 'Site Reliability Engineer',
    role: 'SRE',
    description: 'Reliability, monitoring, incident response, SLOs, error budgets.',
    capabilities: ['monitoring', 'incident-response', 'slo-definition', 'error-budgets', 'postmortems'],
    tools: ['prometheus', 'grafana', 'pagerduty', 'opsgenie'],
  },
  'release-manager': {
    id: 'release-manager',
    name: 'Release Manager',
    role: 'Release Manager',
    description: 'Release planning, deployment coordination, rollback procedures.',
    capabilities: ['release-planning', 'deployment-coordination', 'rollback-procedures', 'change-management'],
    tools: ['jira', 'confluence', 'slack'],
  },

  // --- Verification ---
  'security-auditor': {
    id: 'security-auditor',
    name: 'Security Auditor',
    role: 'Security Auditor',
    description: 'Security audits, compliance checks, penetration testing.',
    capabilities: ['security-audit', 'compliance', 'penetration-testing', 'vulnerability-assessment'],
    tools: ['owasp-zap', 'nessus', 'qualys'],
  },
  'performance-engineer': {
    id: 'performance-engineer',
    name: 'Performance Engineer',
    role: 'Performance Engineer',
    description: 'Performance testing, profiling, optimization, load testing.',
    capabilities: ['load-testing', 'profiling', 'optimization', 'benchmarking', 'capacity-planning'],
    tools: ['jmeter', 'gatling', 'k6', 'new-relic'],
  },

  // --- Documentation ---
  'technical-writer': {
    id: 'technical-writer',
    name: 'Technical Writer',
    role: 'Technical Writer',
    description: 'API documentation, user guides, architecture docs, release notes.',
    capabilities: ['api-docs', 'user-guides', 'architecture-docs', 'release-notes'],
    tools: ['docusaurus', 'swaggo', 'readme'],
  },
};

// ---------------------------------------------------------------------------
// Expert Group Templates
// ---------------------------------------------------------------------------

export const EXPERT_TEAM_TEMPLATES: Record<string, string[]> = {
  'default': ['pm', 'engineer', 'qa'],
  'fullstack': ['pm', 'fullstack-dev', 'qa'],
  'web': ['pm', 'frontend-dev', 'backend-dev', 'qa'],
  'mobile': ['pm', 'mobile-dev', 'qa'],
  'data': ['pm', 'data-engineer', 'dba', 'qa'],
  'ml': ['pm', 'ml-engineer', 'data-engineer', 'qa'],
  'security': ['security-engineer', 'security-auditor', 'dba'],
  'architecture': ['architect', 'tech-lead', 'dba', 'devops'],
  'code-review': ['code-reviewer', 'senior-dev', 'tech-lead'],
  'performance': ['performance-engineer', 'sre', 'devops'],
  'deploy': ['devops', 'sre', 'release-manager', 'qa'],
};

// ---------------------------------------------------------------------------
// Utility Functions
// ---------------------------------------------------------------------------

/**
 * Get an expert by ID (alias for getExpertById)
 */
export function getExpert(id: string): Expert | undefined {
  return EXPERT_REGISTRY[id];
}

/**
 * Get an expert by ID, returns null if not found
 */
export function getExpertById(id: string): Expert | null {
  return EXPERT_REGISTRY[id] ?? null;
}

/**
 * Get all experts in a category
 */
export function getExpertsByCategory(category: string): Expert[] {
  return Object.values(EXPERT_REGISTRY).filter(e =>
    (e.capabilities ?? []).some(c => c.startsWith(category))
  );
}

/**
 * Get experts by team template
 */
export function getExpertTeam(template: string | string[]): Expert[] {
  if (Array.isArray(template)) {
    return template.map(id => getExpert(id)).filter((e): e is Expert => e !== undefined);
  }
  const ids = EXPERT_TEAM_TEMPLATES[template] ?? template.split(',').map(s => s.trim());
  return ids.map(id => getExpert(id)).filter((e): e is Expert => e !== undefined);
}

/**
 * List all available expert IDs
 */
export function listExpertIds(): string[] {
  return Object.keys(EXPERT_REGISTRY);
}

/**
 * Search experts by capability
 */
export function searchExperts(query: string): Expert[] {
  const q = query.toLowerCase();
  return Object.values(EXPERT_REGISTRY).filter(e =>
    e.name.toLowerCase().includes(q) ||
    e.role.toLowerCase().includes(q) ||
    e.description.toLowerCase().includes(q) ||
    (e.capabilities ?? []).some(c => c.toLowerCase().includes(q))
  );
}

// ============================================================================
// Additional Expert Utilities (enhanced for plugin)
// ============================================================================

/**
 * List all experts, optionally filtered by role
 * @param role - Optional role filter (e.g., 'architect', 'planner', 'qa')
 */
export function listExperts(role?: string): Expert[] {
  const all = Object.values(EXPERT_REGISTRY);
  if (!role) return all;
  return all.filter(e => e.role.toLowerCase() === role.toLowerCase());
}

/**
 * Get experts by role category (alias for listExperts with role filter)
 */
export function getExpertsByRole(role: string): Expert[] {
  return listExperts(role);
}

/**
 * Count experts by role
 */
export function countExpertsByRole(): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const expert of Object.values(EXPERT_REGISTRY)) {
    counts[expert.role] = (counts[expert.role] ?? 0) + 1;
  }
  return counts;
}

/**
 * Get all available experts
 */
export function getAvailableExperts(): Expert[] {
  return Object.values(EXPERT_REGISTRY).filter(e => e.available !== false);
}

/**
 * Get expert statistics
 */
export function getExpertStats(): {
  total: number
  byRole: Record<string, number>
  available: number
} {
  const byRole = countExpertsByRole();
  const available = getAvailableExperts().length;
  return {
    total: Object.keys(EXPERT_REGISTRY).length,
    byRole,
    available,
  };
}

/**
 * Format expert as markdown
 */
export function formatExpertAsMarkdown(expert: Expert): string {
  const lines = [
    `### ${expert.name}`,
    `**Role:** ${expert.role}`,
    `**ID:** ${expert.id}`,
    '',
    expert.description,
    '',
    `**Capabilities:**`,
    ...(expert.capabilities ?? []).map(c => `- ${c}`),
    '',
    `**Tools:**`,
    ...(expert.tools ?? []).map(t => `- ${t}`),
  ];
  return lines.join('\n');
}

/**
 * List all experts as formatted markdown
 */
export function listExpertsAsMarkdown(role?: string): string {
  const experts = listExperts(role);
  if (experts.length === 0) return 'No experts found.';

  const grouped: Record<string, Expert[]> = {};
  for (const e of experts) {
    if (!grouped[e.role]) grouped[e.role] = [];
    grouped[e.role].push(e);
  }

  const lines: string[] = ['## Expert Library'];
  if (role) lines.push(`Showing experts with role: **${role}**`);
  lines.push('');

  for (const [roleName, roleExperts] of Object.entries(grouped)) {
    lines.push(`### ${roleName.charAt(0).toUpperCase() + roleName.slice(1)} (${roleExperts.length})`);
    for (const e of roleExperts) {
      lines.push(`- **${e.name}** (${e.id}): ${e.description.slice(0, 80)}...`);
    }
    lines.push('');
  }

  return lines.join('\n');
}
