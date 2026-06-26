/**
 * Unit tests for cross-border-intel skill
 */
import { describe, it, expect } from 'vitest';
import { skill, healthCheck, 
// Core
generateLocalId, nowUtc, todayUtc, 
// Watchlist
addAmazonWatchlistItem, addTiktokWatchlistItem, listActiveWatchlists, 
// API
fetchAmazonProduct, searchTiktokVideos, 
// Amazon
runAmazonScan, 
// TikTok
runTiktokScan, 
// Reporting
generateDailyReport, generateWeeklyReport, } from './index.js';
describe('cross-border-intel skill', () => {
    describe('skill manifest', () => {
        it('should have correct metadata', () => {
            expect(skill.name).toBe('cross-border-intel');
            expect(skill.version).toBe('0.1.0');
            expect(skill.installSlug).toBe('beansmile/skill-cross-border-intel');
            expect(skill.npmPackageName).toBe('@beansmile/skill-cross-border-intel');
            expect(skill.owner).toBe('beansmile');
            expect(skill.category).toBe('business');
            expect(skill.icon).toBe('🔍');
        });
        it('should have a description', () => {
            expect(skill.description).toBeTruthy();
            expect(skill.description).toContain('跨境');
        });
    });
    describe('health check', () => {
        it('should return ok status', () => {
            const health = healthCheck();
            expect(health.status).toBe('ok');
            expect(health.version).toBe('0.1.0');
        });
    });
    describe('utility functions', () => {
        it('should generate unique IDs', () => {
            const id1 = generateLocalId();
            const id2 = generateLocalId();
            expect(id1).not.toBe(id2);
            expect(id1).toMatch(/^\d+-\d+-\d+$/);
        });
        it('should return UTC time in ISO format', () => {
            const now = nowUtc();
            expect(now).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/);
        });
        it('should return today\'s date', () => {
            const today = todayUtc();
            expect(today).toMatch(/^\d{4}-\d{2}-\d{2}$/);
        });
    });
    describe('exports', () => {
        it('should export watchlist functions', () => {
            expect(typeof addAmazonWatchlistItem).toBe('function');
            expect(typeof addTiktokWatchlistItem).toBe('function');
            expect(typeof listActiveWatchlists).toBe('function');
        });
        it('should export API functions', () => {
            expect(typeof fetchAmazonProduct).toBe('function');
            expect(typeof searchTiktokVideos).toBe('function');
        });
        it('should export scan functions', () => {
            expect(typeof runAmazonScan).toBe('function');
            expect(typeof runTiktokScan).toBe('function');
        });
        it('should export reporting functions', () => {
            expect(typeof generateDailyReport).toBe('function');
            expect(typeof generateWeeklyReport).toBe('function');
        });
    });
});
