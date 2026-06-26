import {
  pgTable,
  uuid,
  text,
  integer,
  boolean,
  timestamp,
  jsonb,
  pgEnum,
} from "drizzle-orm/pg-core";

export const scanStatusEnum = pgEnum("scan_status", [
  "queued",
  "scanning",
  "complete",
  "failed",
]);

export const skillSourceEnum = pgEnum("skill_source", [
  "local",
  "clawhub",
  "url",
]);

export const severityEnum = pgEnum("severity", [
  "critical",
  "high",
  "medium",
  "low",
]);

export const planEnum = pgEnum("plan", ["free", "pro", "team"]);

export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  githubId: text("github_id").unique().notNull(),
  githubUsername: text("github_username").notNull(),
  email: text("email"),
  plan: planEnum("plan").default("free"),
  apiKey: text("api_key").unique(),
  createdAt: timestamp("created_at").defaultNow(),
});

export const scans = pgTable("scans", {
  id: uuid("id").primaryKey().defaultRandom(),
  skillName: text("skill_name").notNull(),
  skillVersion: text("skill_version"),
  skillSource: skillSourceEnum("skill_source").default("local"),
  status: scanStatusEnum("status").default("queued"),
  riskScore: integer("risk_score"),
  riskGrade: text("risk_grade"),
  findingsCount: jsonb("findings_count"),
  userId: uuid("user_id").references(() => users.id),
  createdAt: timestamp("created_at").defaultNow(),
  completedAt: timestamp("completed_at"),
});

export const findings = pgTable("findings", {
  id: uuid("id").primaryKey().defaultRandom(),
  scanId: uuid("scan_id")
    .references(() => scans.id)
    .notNull(),
  category: text("category").notNull(),
  severity: severityEnum("severity").notNull(),
  title: text("title").notNull(),
  description: text("description").notNull(),
  evidence: text("evidence"),
  lineNumber: integer("line_number"),
  analysisPass: text("analysis_pass"),
  createdAt: timestamp("created_at").defaultNow(),
});

export const semanticUsage = pgTable("semantic_usage", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id")
    .references(() => users.id)
    .notNull(),
  periodStart: timestamp("period_start").notNull(),
  scanCount: integer("scan_count").default(0).notNull(),
});

export const webhooks = pgTable("webhooks", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id")
    .references(() => users.id)
    .notNull(),
  url: text("url").notNull(),
  events: text("events").array().notNull(),
  active: boolean("active").default(true),
  createdAt: timestamp("created_at").defaultNow(),
});
