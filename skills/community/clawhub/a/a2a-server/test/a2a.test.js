/**
 * A2A Server 完整测试套件 - Jest 版本
 * 
 * 测试覆盖:
 * - 服务器启动/停止
 * - Agent 注册/注销/心跳
 * - RPC 调用/响应
 * - 能力发现
 * - 离线消息队列
 * - 错误处理
 * - 并发连接
 */

const { A2AServer } = require('../src/server');
const { A2AClient } = require('../src/client');

const TEST_PORT = 18080;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

describe('A2A Server 测试套件', () => {
  let server;
  let clients = [];

  beforeEach(async () => {
    // 确保之前的实例已停止
    if (server) {
      try { await server.stop(); } catch (e) {}
      await sleep(300);
    }
    
    server = new A2AServer({ 
      port: TEST_PORT, 
      verbose: false,
      heartbeatInterval: 5000
    });
    await server.start();
    await sleep(300);
    clients = [];
  });

  afterEach(async () => {
    // 先断开所有客户端
    for (const client of clients) {
      try { 
        client.options.maxReconnectAttempts = 0;
        if (client.ws) {
          client.ws.terminate();
        }
      } catch (e) {}
    }
    clients = [];
    await sleep(200);
    
    // 再停止服务器
    if (server) {
      try { await server.stop(); } catch (e) {}
      await sleep(300);
    }
  });

  // ========== 服务器基础测试 ==========
  describe('服务器基础功能', () => {
    test('服务器启动成功', async () => {
      expect(server.wss).toBeDefined();
      expect(server.options.port).toBe(TEST_PORT);
    });

    test('获取服务器统计信息', async () => {
      const stats = server.getStats();
      expect(stats).toHaveProperty('totalConnections');
      expect(stats).toHaveProperty('totalMessages');
      expect(stats).toHaveProperty('activeAgents');
      expect(stats).toHaveProperty('uptime');
      expect(stats).toHaveProperty('memoryUsage');
      expect(stats.activeAgents).toBe(0);
      expect(stats.totalConnections).toBe(0);
    });

    test('服务器停止后清理资源', async () => {
      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'test-client',
        verbose: false
      });
      clients.push(client);
      
      await client.connect();
      await sleep(500);
      
      expect(server.getAgents().length).toBe(1);
      
      await server.stop();
      await sleep(200);
      
      expect(server.getAgents().length).toBe(0);
      expect(server.agents.size).toBe(0);
    });
  });

  // ========== Agent 注册/注销/心跳测试 ==========
  describe('Agent 注册/注销/心跳', () => {
    test('客户端连接并自动注册', async () => {
      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'test-agent',
        capabilities: ['test'],
        verbose: false
      });
      clients.push(client);

      await client.connect();
      await sleep(800);

      expect(client.connected).toBe(true);

      const agents = server.getAgents();
      expect(agents.length).toBe(1);
      expect(agents[0].agentId).toBe('test-agent');
      expect(agents[0].capabilities).toContain('test');
    });

    test('多个 Agent 注册', async () => {
      const client1 = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'agent-1',
        capabilities: ['cap1'],
        verbose: false
      });
      const client2 = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'agent-2',
        capabilities: ['cap2'],
        verbose: false
      });
      clients.push(client1, client2);

      await Promise.all([client1.connect(), client2.connect()]);
      await sleep(800);

      const agents = server.getAgents();
      expect(agents.length).toBe(2);
    });

    test('相同 agentId 覆盖注册', async () => {
      const client1 = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'same-id',
        capabilities: ['old-cap'],
        verbose: false
      });
      clients.push(client1);

      await client1.connect();
      await sleep(500);

      const client2 = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'same-id',
        capabilities: ['new-cap'],
        verbose: false
      });
      clients.push(client2);

      await client2.connect();
      await sleep(500);

      const agents = server.getAgents();
      expect(agents.length).toBe(1);
      expect(agents[0].capabilities).toContain('new-cap');
    });

    test('心跳机制保持连接', async () => {
      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'heartbeat-test',
        verbose: false
      });
      clients.push(client);

      await client.connect();
      await sleep(500);

      const agentBefore = server.agents.get('heartbeat-test');
      expect(agentBefore).toBeDefined();
      const lastHeartbeatBefore = agentBefore.lastHeartbeat;

      client.heartbeat();
      await sleep(300);

      const agentAfter = server.agents.get('heartbeat-test');
      expect(agentAfter.lastHeartbeat).toBeGreaterThanOrEqual(lastHeartbeatBefore);
    });

    test('心跳超时检测', async () => {
      await server.stop();
      await sleep(200);
      
      server = new A2AServer({
        port: TEST_PORT,
        verbose: false,
        heartbeatInterval: 200
      });
      await server.start();
      await sleep(200);

      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'timeout-test',
        verbose: false
      });
      clients.push(client);

      await client.connect();
      await sleep(500);
      
      expect(server.getAgents().length).toBe(1);

      client.options.maxReconnectAttempts = 0;
      client.ws.terminate();
      
      await sleep(1000);

      expect(server.getAgents().length).toBe(0);
    });
  });

  // ========== RPC 调用/响应测试 ==========
  describe('RPC 调用/响应', () => {
    test('在线 Agent 之间的 RPC 调用', async () => {
      const callee = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'callee',
        capabilities: ['calculator'],
        verbose: false
      });
      const caller = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'caller',
        verbose: false
      });
      clients.push(callee, caller);

      await Promise.all([callee.connect(), caller.connect()]);
      await sleep(500);

      callee.on('call', async (message) => {
        if (message.payload.action === 'add') {
          const result = message.payload.a + message.payload.b;
          callee.ws.send(JSON.stringify({
            type: 'response',
            to: message.from,
            correlationId: message.correlationId,
            payload: { result }
          }));
        }
      });

      const result = await caller.call('callee', {
        action: 'add',
        a: 123,
        b: 456
      }, { timeout: 5000 });

      expect(result).toBeDefined();
      expect(result.result).toBe(579);
    });

    test('RPC 调用超时', async () => {
      const caller = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'timeout-caller',
        verbose: false
      });
      clients.push(caller);

      await caller.connect();
      await sleep(500);

      await expect(
        caller.call('nonexistent', { test: 'data' }, { timeout: 1000 })
      ).rejects.toThrow();
    });
  });

  // ========== 能力发现测试 ==========
  describe('能力发现', () => {
    test('发现所有 Agent', async () => {
      const agent1 = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'discoverable-1',
        capabilities: ['search', 'analyze'],
        verbose: false
      });
      const agent2 = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'discoverable-2',
        capabilities: ['calculator'],
        verbose: false
      });
      const discoverer = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'discoverer',
        verbose: false
      });
      clients.push(agent1, agent2, discoverer);

      await Promise.all([agent1.connect(), agent2.connect(), discoverer.connect()]);
      await sleep(500);

      const allAgents = await discoverer.discover();
      expect(allAgents.length).toBeGreaterThanOrEqual(2);
    });

    test('按能力筛选', async () => {
      const agent1 = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'search-agent',
        capabilities: ['search', 'analyze'],
        verbose: false
      });
      const agent2 = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'calc-agent',
        capabilities: ['calculator'],
        verbose: false
      });
      const discoverer = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'cap-discoverer',
        verbose: false
      });
      clients.push(agent1, agent2, discoverer);

      await Promise.all([agent1.connect(), agent2.connect(), discoverer.connect()]);
      await sleep(500);

      const searchAgents = await discoverer.discover({ capability: 'search' });
      expect(searchAgents.length).toBe(1);
      expect(searchAgents[0].agentId).toBe('search-agent');

      const calcAgents = await discoverer.discover({ capability: 'calculator' });
      expect(calcAgents.length).toBe(1);
      expect(calcAgents[0].agentId).toBe('calc-agent');
    });
  });

  // ========== 离线消息队列测试 ==========
  describe('离线消息队列', () => {
    test('消息队列给离线 Agent', async () => {
      const sender = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'queue-sender',
        verbose: false
      });
      clients.push(sender);

      await sender.connect();
      await sleep(500);

      try {
        await sender.call('offline-agent', { test: 'queued' }, { timeout: 1000 });
      } catch (error) {
        expect(error.message).toMatch(/offline|timeout/i);
      }

      expect(server.messageQueue.has('offline-agent')).toBe(true);
      const queue = server.messageQueue.get('offline-agent');
      expect(queue.length).toBeGreaterThan(0);
    });
  });

  // ========== 错误处理测试 ==========
  describe('错误处理', () => {
    test('处理无效消息格式', async () => {
      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'error-client',
        verbose: false
      });
      clients.push(client);

      await client.connect();
      await sleep(500);

      client.ws.send('invalid json');
      await sleep(200);

      expect(client.connected).toBe(true);
    });

    test('调用不存在的 Agent', async () => {
      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'nonexist-caller',
        verbose: false
      });
      clients.push(client);

      await client.connect();
      await sleep(500);

      await expect(
        client.call('definitely-not-exist', { test: 'data' }, { timeout: 1000 })
      ).rejects.toThrow();
    });
  });

  // ========== 并发连接测试 ==========
  describe('并发连接', () => {
    test('多个并发连接', async () => {
      const clientCount = 10;
      const newClients = [];

      for (let i = 0; i < clientCount; i++) {
        const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
          agentId: `concurrent-${i}`,
          capabilities: [`cap-${i}`],
          verbose: false
        });
        newClients.push(client);
        clients.push(client);
      }

      await Promise.all(newClients.map(c => c.connect()));
      await sleep(800);

      const agents = server.getAgents();
      expect(agents.length).toBe(clientCount);
    });

    test('并发 RPC 调用', async () => {
      const callee = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'concurrent-callee',
        capabilities: ['echo'],
        verbose: false
      });
      clients.push(callee);

      await callee.connect();
      await sleep(500);

      callee.on('call', async (message) => {
        callee.ws.send(JSON.stringify({
          type: 'response',
          to: message.from,
          correlationId: message.correlationId,
          payload: { echo: message.payload }
        }));
      });

      const caller = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'concurrent-caller',
        verbose: false
      });
      clients.push(caller);

      await caller.connect();
      await sleep(500);

      const calls = [];
      for (let i = 0; i < 10; i++) {
        calls.push(caller.call('concurrent-callee', { index: i }, { timeout: 5000 }));
      }

      const results = await Promise.all(calls);
      expect(results.length).toBe(10);
      results.forEach((result, i) => {
        expect(result.echo.index).toBe(i);
      });
    });
  });

  // ========== 客户端方法测试 ==========
  describe('客户端方法', () => {
    test('获取状态', async () => {
      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'status-test',
        verbose: false
      });
      clients.push(client);

      let status = client.getStatus();
      expect(status.connected).toBe(false);
      expect(status.agentId).toBe('status-test');

      await client.connect();
      await sleep(800);

      status = client.getStatus();
      expect(status.connected).toBe(true);
      expect(status.agentId).toBe('status-test');
    });

    test('发送消息', async () => {
      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'send-test',
        verbose: false
      });
      clients.push(client);
      await client.connect();
      await sleep(500);
      
      client.send({ type: 'custom', data: 'test' });
      await sleep(200);
      expect(client.connected).toBe(true);
    });

    test('事件监听', async () => {
      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'event-test',
        verbose: false
      });
      clients.push(client);
      
      const events = [];
      client.on('registered', () => events.push('registered'));
      
      await client.connect();
      await sleep(800);
      
      expect(events).toContain('registered');
    });
  });

  // ========== 服务器方法测试 ==========
  describe('服务器方法', () => {
    test('广播消息', async () => {
      const client1 = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'broadcast-1',
        verbose: false
      });
      const client2 = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'broadcast-2',
        verbose: false
      });
      clients.push(client1, client2);
      
      await Promise.all([client1.connect(), client2.connect()]);
      await sleep(500);
      
      server.broadcast({ message: 'test' });
      await sleep(200);
      
      expect(server.getAgents().length).toBe(2);
    });

    test('获取单个 Agent 信息', async () => {
      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'single-agent',
        capabilities: ['test'],
        metadata: { version: '1.0' },
        verbose: false
      });
      clients.push(client);
      
      await client.connect();
      await sleep(500);
      
      const agent = server.getAgent('single-agent');
      expect(agent).toBeDefined();
      expect(agent.agentId).toBe('single-agent');
      expect(agent.capabilities).toContain('test');
      expect(agent.metadata.version).toBe('1.0');
    });

    test('检查 Agent 在线状态', async () => {
      const client = new A2AClient(`ws://localhost:${TEST_PORT}`, {
        agentId: 'online-check',
        verbose: false
      });
      clients.push(client);
      
      await client.connect();
      await sleep(500);
      
      expect(server.isAgentOnline('online-check')).toBe(true);
      expect(server.isAgentOnline('nonexistent')).toBe(false);
    });
  });
});