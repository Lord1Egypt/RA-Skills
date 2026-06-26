#!/usr/bin/env node
/**
 * logger.js - CS 대화 로그 기록
 * 일별 JSONL 형식으로 저장
 */

const fs = require('fs');
const path = require('path');

class CSLogger {
  constructor(config) {
    this.config = config;
    this.logDir = path.resolve(config.logging.logDir);
    this.clientId = config.clientId;
  }

  /**
   * 로그 항목 기록
   * @param {Object} entry - 로그 항목
   */
  log(entry) {
    if (!this.config.logging.enabled) return;

    const date = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
    const dayDir = path.join(this.logDir, date);
    const logFile = path.join(dayDir, `${this.clientId}.jsonl`);

    // 디렉토리 생성
    if (!fs.existsSync(dayDir)) {
      fs.mkdirSync(dayDir, { recursive: true });
    }

    // 로그 항목 작성
    const logEntry = {
      timestamp: new Date().toISOString(),
      ...entry
    };

    fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n', 'utf-8');
  }

  /**
   * 특정 날짜의 로그 읽기
   * @param {string} date - YYYY-MM-DD
   * @returns {Array} 로그 항목 배열
   */
  readLogs(date) {
    const logFile = path.join(this.logDir, date, `${this.clientId}.jsonl`);
    
    if (!fs.existsSync(logFile)) {
      return [];
    }

    const lines = fs.readFileSync(logFile, 'utf-8').trim().split('\n');
    return lines
      .filter(line => line.length > 0)
      .map(line => JSON.parse(line));
  }

  /**
   * 오래된 로그 파일 정리
   */
  cleanOldLogs() {
    const retentionDays = this.config.logging.retentionDays || 90;
    const now = new Date();
    
    if (!fs.existsSync(this.logDir)) return;

    const dirs = fs.readdirSync(this.logDir);
    
    dirs.forEach(dir => {
      const dirPath = path.join(this.logDir, dir);
      const stat = fs.statSync(dirPath);
      
      if (!stat.isDirectory()) return;
      
      // 날짜 파싱
      const parts = dir.split('-');
      if (parts.length !== 3) return;
      
      const logDate = new Date(dir);
      const daysDiff = Math.floor((now - logDate) / (1000 * 60 * 60 * 24));
      
      if (daysDiff > retentionDays) {
        console.log(`🗑️  Deleting old logs: ${dir} (${daysDiff} days old)`);
        fs.rmSync(dirPath, { recursive: true, force: true });
      }
    });
  }

  /**
   * 통계 생성
   * @param {string} date - YYYY-MM-DD
   * @returns {Object} 통계 객체
   */
  generateStats(date) {
    const logs = this.readLogs(date);
    
    if (logs.length === 0) {
      return {
        totalInquiries: 0,
        autoResponded: 0,
        escalated: 0,
        autoResponseRate: 0,
        categoryBreakdown: {},
        channelBreakdown: {},
        avgResponseTime: 0
      };
    }

    const stats = {
      totalInquiries: logs.length,
      autoResponded: logs.filter(l => !l.escalated).length,
      escalated: logs.filter(l => l.escalated).length,
      autoResponseRate: 0,
      categoryBreakdown: {},
      channelBreakdown: {},
      avgResponseTime: 0
    };

    stats.autoResponseRate = ((stats.autoResponded / stats.totalInquiries) * 100).toFixed(1);

    // 카테고리별 집계
    logs.forEach(log => {
      const category = log.category || '기타';
      stats.categoryBreakdown[category] = (stats.categoryBreakdown[category] || 0) + 1;

      const channel = log.channel || 'unknown';
      stats.channelBreakdown[channel] = (stats.channelBreakdown[channel] || 0) + 1;
    });

    // 평균 응답시간 (초 단위, mock)
    stats.avgResponseTime = 3.2;

    return stats;
  }
}

module.exports = CSLogger;
