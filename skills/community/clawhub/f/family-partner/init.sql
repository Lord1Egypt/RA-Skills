-- Family Partner Database Initialization Script
-- Version: v3.0
-- Last Updated: 2026-03-02

-- Events table
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    participants TEXT,  -- Comma-separated: "Dad,Mom,Ethan"
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_events_time ON events(start_time);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT DEFAULT 'todo',  -- todo, shopping
    status TEXT DEFAULT 'pending',
    assignee TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);

-- Labor table (Invisible labor tracking)
CREATE TABLE IF NOT EXISTS labor (
    id TEXT PRIMARY KEY,
    member_name TEXT NOT NULL,
    type TEXT NOT NULL,  -- cooking, cleaning, childcare, etc.
    duration INTEGER NOT NULL,  -- minutes
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_labor_date ON labor(date);
CREATE INDEX IF NOT EXISTS idx_labor_member ON labor(member_name, date);

-- Family time table
CREATE TABLE IF NOT EXISTS family_time (
    id TEXT PRIMARY KEY,
    activity TEXT NOT NULL,
    participants TEXT,
    duration INTEGER,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Milestones table
CREATE TABLE IF NOT EXISTS milestones (
    id TEXT PRIMARY KEY,
    member_name TEXT,
    title TEXT NOT NULL,
    category TEXT,  -- first, achievement, growth, skill, life, other
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_milestones_member ON milestones(member_name);
CREATE INDEX IF NOT EXISTS idx_milestones_category ON milestones(category);

-- Anniversaries table
CREATE TABLE IF NOT EXISTS anniversaries (
    id TEXT PRIMARY KEY,
    member_name TEXT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,  -- MM-DD format
    year INTEGER,
    type TEXT DEFAULT 'birthday',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_anniversaries_date ON anniversaries(date);

-- Memories table
CREATE TABLE IF NOT EXISTS memories (
    id TEXT PRIMARY KEY,
    member_name TEXT,
    type TEXT NOT NULL,  -- preference, dislike, allergy
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_memories_member ON memories(member_name);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);

-- Votes table (Simplified version - uses description field)
CREATE TABLE IF NOT EXISTS votes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,  -- Stores options and voting records
    status TEXT DEFAULT 'active',
    created_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_votes_status ON votes(status);

-- Challenges table (Simplified version - uses description field)
CREATE TABLE IF NOT EXISTS challenges (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,  -- Stores participant progress
    goal INTEGER,
    status TEXT DEFAULT 'active',
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_challenges_status ON challenges(status);
