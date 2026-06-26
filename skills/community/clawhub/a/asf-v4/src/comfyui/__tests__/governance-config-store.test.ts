/**
 * 治理配置存储单元测试
 */

import { InMemoryConfigStore, ConfigManager } from '../governance-config-store';

describe('InMemoryConfigStore', () => {
  let store: InMemoryConfigStore;

  beforeEach(() => {
    store = new InMemoryConfigStore();
  });

  describe('save', () => {
    it('should save valid configuration', async () => {
      const snapshot = store.createDefaultSnapshot('test-user');

      await expect(store.save(snapshot)).resolves.not.toThrow();
    });

    it('should reject invalid configuration', async () => {
      const snapshot = store.createDefaultSnapshot('test-user');
      snapshot.governance.maxDurationSeconds = 100; // Invalid

      await expect(store.save(snapshot)).rejects.toThrow();
    });
  });

  describe('getActive', () => {
    it('should return undefined when no active config', async () => {
      const active = await store.getActive();
      expect(active).toBeUndefined();
    });

    it('should return active config after activation', async () => {
      const snapshot = store.createDefaultSnapshot('test-user');
      await store.save(snapshot);
      await store.activate(snapshot.id);

      const active = await store.getActive();
      expect(active).toBeDefined();
      expect(active?.isActive).toBe(true);
    });
  });

  describe('activate', () => {
    it('should activate configuration', async () => {
      const snapshot = store.createDefaultSnapshot('test-user');
      await store.save(snapshot);

      await store.activate(snapshot.id);

      const active = await store.getActive();
      expect(active?.id).toBe(snapshot.id);
    });

    it('should deactivate previous active config', async () => {
      const snapshot1 = store.createDefaultSnapshot('user1');
      await store.save(snapshot1);
      await store.activate(snapshot1.id);

      const snapshot2 = store.createDefaultSnapshot('user2');
      snapshot2.id = 'config_2';
      await store.save(snapshot2);
      await store.activate(snapshot2.id);

      const active = await store.getActive();
      expect(active?.id).toBe('config_2');
    });
  });

  describe('list', () => {
    it('should list all configurations', async () => {
      const snapshot1 = store.createDefaultSnapshot('user1');
      const snapshot2 = store.createDefaultSnapshot('user2');
      snapshot2.id = 'config_2';

      await store.save(snapshot1);
      await store.save(snapshot2);

      const configs = await store.list();
      expect(configs.length).toBe(2);
    });
  });
});

describe('ConfigManager', () => {
  let manager: ConfigManager;
  let store: InMemoryConfigStore;

  beforeEach(() => {
    store = new InMemoryConfigStore();
    manager = new ConfigManager(store);
  });

  describe('initialize', () => {
    it('should create default configuration', async () => {
      const config = await manager.initialize('test-user');

      expect(config.version.version).toBe('1.0.0');
      expect(config.isActive).toBe(true);
    });

    it('should return existing config if already initialized', async () => {
      await manager.initialize('user1');
      const config2 = await manager.initialize('user2');

      expect(config2.version.createdBy).toBe('user1');
    });
  });

  describe('getCurrentConfig', () => {
    it('should throw error when no config', async () => {
      await expect(manager.getCurrentConfig()).rejects.toThrow();
    });

    it('should return active config', async () => {
      await manager.initialize('test-user');
      const config = await manager.getCurrentConfig();

      expect(config).toBeDefined();
    });
  });

  describe('cloneConfig', () => {
    it('should clone configuration with new version', async () => {
      await manager.initialize('test-user');
      const configs = await manager.listConfigs();
      const baseConfig = configs[0];

      const cloned = await manager.cloneConfig(
        baseConfig.id,
        '1.1.0',
        'Test clone'
      );

      expect(cloned.version.version).toBe('1.1.0');
      expect(cloned.isActive).toBe(false);
    });
  });

  describe('updateConfig', () => {
    it('should update configuration', async () => {
      await manager.initialize('test-user');
      const configs = await manager.listConfigs();
      const config = configs[0];

      const updated = await manager.updateConfig(config.id, {
        governance: { ...config.governance, dailyQuota: 200 },
      });

      expect(updated.governance.dailyQuota).toBe(200);
    });
  });

  describe('exportConfig', () => {
    it('should export config as JSON', async () => {
      await manager.initialize('test-user');
      const configs = await manager.listConfigs();

      const json = await manager.exportConfig(configs[0].id);
      const parsed = JSON.parse(json);

      expect(parsed.id).toBe(configs[0].id);
    });
  });

  describe('importConfig', () => {
    it('should import config from JSON', async () => {
      await manager.initialize('test-user');
      const configs = await manager.listConfigs();
      const json = await manager.exportConfig(configs[0].id);

      const imported = await manager.importConfig(json);

      expect(imported.id).toBeDefined();
      // 导入的配置会保留原 ID，但会创建新条目
      expect(imported.version.version).toBe(configs[0].version.version);
    });
  });
});
