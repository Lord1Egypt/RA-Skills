import { OnePanelConfig } from "./types/config.js";
import {
  ContainerAPI,
  ImageAPI,
  NetworkAPI,
  VolumeAPI,
  ComposeAPI,
  AppAPI,
  WebsiteAPI,
  FileAPI,
  DatabaseAPI,
  SystemAPI,
  CronjobAPI,
  FirewallAPI,
  ProcessAPI,
  SSHAPI,
  TerminalAPI,
  BackupAPI,
  BackupAccountAPI,
  SettingsAPI,
  LogsAPI,
  RuntimeAPI,
  Fail2BanAPI,
  DiskAPI,
  DashboardAPI,
  MonitorAPI,
  DeviceAPI,
  FTPAPI,
  ClamAPI,
  PHPAPI,
  HostAPI,
  RecycleBinAPI,
  SnapshotAPI,
  TaskAPI,
  OpenRestyAPI,
  GPUAPI,
  NodeAPI,
  AIAPI,
  OllamaAPI,
} from "./api/index.js";

export class OnePanelClient {
  private config: OnePanelConfig;

  // API modules
  public containers: ContainerAPI;
  public images: ImageAPI;
  public networks: NetworkAPI;
  public volumes: VolumeAPI;
  public composes: ComposeAPI;
  public apps: AppAPI;
  public websites: WebsiteAPI;
  public files: FileAPI;
  public databases: DatabaseAPI;
  public system: SystemAPI;
  public cronjobs: CronjobAPI;
  public firewall: FirewallAPI;
  public process: ProcessAPI;
  public ssh: SSHAPI;
  public terminal: TerminalAPI;
  public backup: BackupAPI;
  public backupAccount: BackupAccountAPI;
  public settings: SettingsAPI;
  public logs: LogsAPI;
  public runtime: RuntimeAPI;
  public fail2ban: Fail2BanAPI;
  public disk: DiskAPI;
  public dashboard: DashboardAPI;
  public monitor: MonitorAPI;
  public device: DeviceAPI;
  public ftp: FTPAPI;
  public clam: ClamAPI;
  public php: PHPAPI;
  public host: HostAPI;
  public recycleBin: RecycleBinAPI;
  public snapshot: SnapshotAPI;
  public task: TaskAPI;
  public openresty: OpenRestyAPI;
  public gpu: GPUAPI;
  public node: NodeAPI;
  public ai: AIAPI;
  public ollama: OllamaAPI;

  constructor(config: OnePanelConfig) {
    this.config = { protocol: "http", ...config };

    // Initialize API modules
    this.containers = new ContainerAPI(this.config);
    this.images = new ImageAPI(this.config);
    this.networks = new NetworkAPI(this.config);
    this.volumes = new VolumeAPI(this.config);
    this.composes = new ComposeAPI(this.config);
    this.apps = new AppAPI(this.config);
    this.websites = new WebsiteAPI(this.config);
    this.files = new FileAPI(this.config);
    this.databases = new DatabaseAPI(this.config);
    this.system = new SystemAPI(this.config);
    this.cronjobs = new CronjobAPI(this.config);
    this.firewall = new FirewallAPI(this.config);
    this.process = new ProcessAPI(this.config);
    this.ssh = new SSHAPI(this.config);
    this.terminal = new TerminalAPI(this.config);
    this.backup = new BackupAPI(this.config);
    this.backupAccount = new BackupAccountAPI(this.config);
    this.settings = new SettingsAPI(this.config);
    this.logs = new LogsAPI(this.config);
    this.runtime = new RuntimeAPI(this.config);
    this.fail2ban = new Fail2BanAPI(this.config);
    this.disk = new DiskAPI(this.config);
    this.dashboard = new DashboardAPI(this.config);
    this.monitor = new MonitorAPI(this.config);
    this.device = new DeviceAPI(this.config);
    this.ftp = new FTPAPI(this.config);
    this.clam = new ClamAPI(this.config);
    this.php = new PHPAPI(this.config);
    this.host = new HostAPI(this.config);
    this.recycleBin = new RecycleBinAPI(this.config);
    this.snapshot = new SnapshotAPI(this.config);
    this.task = new TaskAPI(this.config);
    this.openresty = new OpenRestyAPI(this.config);
    this.gpu = new GPUAPI(this.config);
    this.node = new NodeAPI(this.config);
    this.ai = new AIAPI(this.config);
    this.ollama = new OllamaAPI(this.config);
  }

  // Backward compatibility - delegate to modules
  // Containers
  listContainers = () => this.containers.list();
  listContainersSimple = () => this.containers.listSimple();
  getContainer = (id: string) => this.containers.get(id);
  inspectContainer = (id: string) => this.containers.inspect(id);
  startContainer = (id: string) => this.containers.start(id);
  stopContainer = (id: string) => this.containers.stop(id);
  restartContainer = (id: string) => this.containers.restart(id);
  pauseContainer = (id: string) => this.containers.pause(id);
  unpauseContainer = (id: string) => this.containers.unpause(id);
  killContainer = (id: string) => this.containers.kill(id);
  removeContainer = (id: string) => this.containers.remove(id);
  createContainer = (config: any) => this.containers.create(config);
  updateContainer = (id: string, config: any) => this.containers.update(id, config);
  renameContainer = (id: string, name: string) => this.containers.rename(id, name);
  upgradeContainer = (id: string, image: string) => this.containers.upgrade(id, image);
  getContainerLogs = (id: string, tail?: number) => this.containers.getLogs(id, tail);
  getContainerStats = (id: string) => this.containers.getStats(id);
  getContainerStatus = () => this.containers.getStatus();
  pruneContainers = () => this.containers.prune();
  cleanContainerLog = (id: string) => this.containers.cleanLog(id);
  getContainerUsers = (name: string) => this.containers.getUsers(name);
  listContainersByImage = (image: string) => this.containers.listByImage(image);
  commitContainer = (id: string, repo: string, tag: string) => this.containers.commit(id, repo, tag);

  // Images
  listImages = () => this.images.list();
  listAllImages = () => this.images.listAll();
  searchImages = () => this.images.search();
  pullImage = (name: string) => this.images.pull(name);
  pushImage = (name: string) => this.images.push(name);
  removeImage = (id: string) => this.images.remove(id);
  buildImage = (dockerfile: string, name: string, path: string) => this.images.build(dockerfile, name, path);
  tagImage = (id: string, repo: string, tag: string) => this.images.tag(id, repo, tag);
  saveImage = (names: string[]) => this.images.save(names);
  loadImage = (path: string) => this.images.load(path);

  // Networks
  listNetworks = () => this.networks.list();
  createNetwork = (name: string, driver?: string) => this.networks.create(name, driver);
  removeNetwork = (id: string) => this.networks.remove(id);

  // Volumes
  listVolumes = () => this.volumes.list();
  createVolume = (name: string) => this.volumes.create(name);
  removeVolume = (id: string) => this.volumes.remove(id);

  // Compose
  listComposes = () => this.composes.list();
  createCompose = (name: string, content: string, path?: string) => this.composes.create(name, content, path);
  removeCompose = (id: number) => this.composes.remove(id);
  startCompose = (id: number) => this.composes.start(id);
  stopCompose = (id: number) => this.composes.stop(id);
  restartCompose = (id: number) => this.composes.restart(id);
  updateCompose = (id: number, content: string) => this.composes.update(id, content);
  testCompose = (content: string) => this.composes.test(content);
  getComposeEnv = (id: number) => this.composes.getEnv(id);
  cleanComposeLog = (id: number) => this.composes.cleanLog(id);

  // Apps - use apps API directly

  // Websites
  listWebsites = () => this.websites.list();
  createWebsite = (site: any) => this.websites.create(site);
  getWebsite = (id: number) => this.websites.getDetail(id);
  updateWebsite = (site: any) => this.websites.update(site);
  deleteWebsite = (id: number) => this.websites.remove(id);

  // Website Domains
  listWebsiteDomains = (websiteId: number) => this.websites.listDomains(websiteId);
  createWebsiteDomain = (params: any) => this.websites.createDomain(params);
  deleteWebsiteDomain = (params: any) => this.websites.deleteDomain(params);
  updateWebsiteDomain = (params: any) => this.websites.updateDomain(params);

  // SSL Certificates
  listCertificates = () => this.websites.listCertificates();
  getCertificate = (id: number) => this.websites.getCertificate(id);
  createCertificate = (cert: any) => this.websites.createCertificate(cert);
  deleteCertificate = (id: number) => this.websites.deleteCertificate(id);
  obtainSSL = (params: any) => this.websites.obtainSSL(params);
  renewSSL = (params: any) => this.websites.renewSSL(params);
  resolveSSL = (params: any) => this.websites.resolveSSL(params);
  uploadSSL = (params: any) => this.websites.uploadSSL(params);
  getWebsiteSSL = (websiteId: number) => this.websites.getWebsiteSSL(websiteId);

  // HTTPS
  getHTTPS = (id: number) => this.websites.getHTTPS(id);
  updateHTTPS = (params: any) => this.websites.updateHTTPS(params);
  applySSL = (params: any) => this.websites.applySSL(params);

  // Nginx
  getNginxConf = (id: number) => this.websites.getNginxConf(id);
  updateNginxConf = (params: any) => this.websites.updateNginxConf(params);

  // Files
  listFiles = (path: string, page?: number, pageSize?: number) => this.files.list(path, page, pageSize);
  searchFiles = (params: any) => this.files.search(params);
  getFileContent = (path: string) => this.files.getContent(path);
  saveFile = (path: string, content: string) => this.files.save(path, content);
  deleteFile = (path: string, forceDelete?: boolean) => this.files.delete(path, forceDelete);
  createDir = (path: string) => this.files.createDir(path);
  createFile = (path: string) => this.files.createFile(path);
  compressFiles = (params: any) => this.files.compress(params);
  decompressFile = (params: any) => this.files.decompress(params);
  moveFile = (params: any) => this.files.move(params);
  renameFile = (params: any) => this.files.rename(params);
  chmodFile = (params: any) => this.files.chmod(params);
  chownFile = (params: any) => this.files.chown(params);
  checkFile = (path: string) => this.files.check(path);
  getFileSize = (path: string) => this.files.getSize(path);
  getFileTree = (path: string) => this.files.getTree(path);
  downloadFile = (path: string) => this.files.download(path);
  uploadFile = (params: any) => this.files.upload(params);
  wgetFile = (url: string, path: string, ignoreCertificate?: boolean) => this.files.wget(url, path, ignoreCertificate);

  // Databases - use databases API directly

  // System
  getSystemInfo = () => this.system.getInfo();
  getSystemMonitor = () => this.system.getMonitor();

  // Cronjobs
  listCronjobs = () => this.cronjobs.list();
  createCronjob = (job: any) => this.cronjobs.create(job);
  deleteCronjob = (id: number) => this.cronjobs.remove(id);

  // Firewall - use firewall API directly

  // Process
  listProcesses = () => this.process.list();
  killProcess = (pid: number) => this.process.kill(pid);

  // SSH
  getSSHConfig = () => this.ssh.getConfig();
  updateSSHConfig = (config: any) => this.ssh.updateConfig(config);

  // Terminal
  execCommand = (command: string, cwd?: string) => this.terminal.execCommand(command, cwd);

  // Backup
  listBackups = () => this.backup.list();
  createBackup = (backup: any) => this.backup.create(backup);
  restoreBackup = (id: number) => this.backup.restore(id);
  deleteBackup = (id: number) => this.backup.remove(id);

  // Backup Account
  listBackupAccounts = () => this.backupAccount.list();
  // Backup Account - use backupAccount API directly

  // Settings
  getSettings = () => this.settings.getAll();
  updateSettings = (settings: any) => this.settings.update(settings);

  // Logs - use logs API directly

  // Runtime - use runtime API directly

  // Fail2ban
  getFail2BanBaseInfo = () => this.fail2ban.getBaseInfo();
  getFail2BanConf = () => this.fail2ban.getConf();
  operateFail2Ban = (params: any) => this.fail2ban.operate(params);
  operateFail2BanSSH = (params: any) => this.fail2ban.operateSSH(params);
  searchFail2BanBannedIPs = (params?: any) => this.fail2ban.searchBannedIPs(params);
  updateFail2BanConf = (params: any) => this.fail2ban.updateConf(params);
  updateFail2BanConfByFile = (content: string) => this.fail2ban.updateConfByFile(content);

  // Disk - use disk API directly

  // Dashboard
  getDashboardBaseInfo = () => this.dashboard.getBaseInfo();
  getDashboardCurrentInfo = () => this.dashboard.getCurrentInfo();
  getDashboardMemo = () => this.dashboard.getMemo();
  updateDashboardMemo = (content: string) => this.dashboard.updateMemo(content);

  // Monitor
  getMonitorData = (params?: any) => this.monitor.getData(params);
  getMonitorSetting = () => this.monitor.getSetting();
  updateMonitorSetting = (setting: any) => this.monitor.updateSetting(setting);
  cleanMonitorData = () => this.monitor.cleanData();

  // Device - use device API directly

  // FTP
  listFTPUsers = () => this.ftp.list();
  getFTPBaseInfo = () => this.ftp.getBaseInfo();
  createFTPUser = (params: any) => this.ftp.create(params);
  updateFTPUser = (params: any) => this.ftp.update(params);
  deleteFTPUser = (id: number) => this.ftp.remove(id);
  operateFTP = (operation: "start" | "stop" | "restart") => this.ftp.operate(operation);
  syncFTPUsers = () => this.ftp.sync();
  getFTPLogs = () => this.ftp.getLogs();

  // ClamAV
  listClamConfigs = () => this.clam.list();
  // Clam - use clam API directly

  // PHP
  listPHPRuntimes = () => this.php.list();
  getPHPConf = (id: number) => this.php.getConf(id);
  updatePHPConf = (id: number, content: string) => this.php.updateConf(id, content);
  listPHPExtensions = (id: number) => this.php.listExtensions(id);
  installPHPExtension = (id: number, extension: string) => this.php.installExtension(id, extension);
  uninstallPHPExtension = (id: number, extension: string) => this.php.uninstallExtension(id, extension);
  getPHPConfFile = (id: number, type: string) => this.php.getConfFile(id, type);
  updatePHPConfFile = (id: number, type: string, content: string) => this.php.updateConfFile(id, type, content);
  updatePHPVersion = (id: number, version: string) => this.php.updateVersion(id, version);

  // Host
  listHosts = () => this.host.list();
  getHost = (id: number) => this.host.getHost(id);
  createHost = (params: any) => this.host.create(params);
  updateHost = (params: any) => this.host.update(params);
  // Host - use host API directly
  getHostSSHLogs = () => this.host.getSSHLogs();

  // RecycleBin
  getRecycleBinStatus = () => this.recycleBin.getStatus();
  listRecycleBin = () => this.recycleBin.list();
  clearRecycleBin = () => this.recycleBin.clear();
  reduceRecycleBin = (name: string) => this.recycleBin.reduce(name);

  // Snapshot
  listSnapshots = () => this.snapshot.list();
  createSnapshot = (params: any) => this.snapshot.create(params);
  deleteSnapshot = (ids: number[]) => this.snapshot.remove(ids);
  updateSnapshotDescription = (id: number, description: string) => this.snapshot.updateDescription(id, description);
  importSnapshot = (params: any) => this.snapshot.import(params);
  loadSnapshot = (id: number) => this.snapshot.load(id);
  recoverSnapshot = (id: number, isNewSnapshot?: boolean) => this.snapshot.recover(id, isNewSnapshot);
  recreateSnapshot = (id: number) => this.snapshot.recreate(id);

  // Task
  getExecutingTaskCount = () => this.task.getExecutingCount();
  getTaskLogs = () => this.task.getLogs();

  // OpenResty (XPack)
  getOpenRestyConf = () => this.openresty.getConf();
  buildOpenResty = (params: any) => this.openresty.build(params);
  updateOpenRestyByFile = (content: string) => this.openresty.updateByFile(content);
  getOpenRestyModules = () => this.openresty.getModules();
  updateOpenRestyModule = (params: any) => this.openresty.updateModule(params);
  getOpenRestyPartialConf = () => this.openresty.getPartialConf();
  getOpenRestyStatus = () => this.openresty.getStatus();
  updateOpenRestyConf = (params: any) => this.openresty.updateConf(params);

  // GPU (XPack)
  getGPUInfo = () => this.gpu.getInfo();
  getGPUMonitorData = (params: any) => this.gpu.getMonitorData(params);

  // Node (XPack)
  getNodeModules = (id: number) => this.node.getModules(id);
  operateNodeModule = (id: number, params: any) => this.node.operateModule(id, params);
  getNodePackageScripts = (id: number, params: any) => this.node.getPackageScripts(id, params);

  // AI Agent (XPack) - use ai API directly
  // MCP Server (XPack) - use ai API directly
  // Ollama (XPack) - use ollama API directly
  closeOllamaModel = (name: string) => this.ollama.close(name);

  // AntiLeech (XPack)
  getAntiLeechConf = (websiteId: number) => this.websites.getAntiLeechConf(websiteId);
  updateAntiLeech = (params: any) => this.websites.updateAntiLeech(params);
}

export { OnePanelConfig } from "./types/config.js";
export type { OnePanelConfig as Config };
