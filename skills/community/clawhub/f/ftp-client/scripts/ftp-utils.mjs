import { Client } from "basic-ftp";

/**
 * Parse FTP_CONNECTION environment variable.
 * Format: host:port,username,password[,active/passive][,ftp/ftps][,explicit/implicit]
 */
export function parseFtpConnection(connStr) {
  if (!connStr) {
    throw new Error(
      "FTP_CONNECTION environment variable is not set.\n" +
      "Format: host:port,username,password[,active/passive][,ftp/ftps][,explicit/implicit]\n" +
      "Example: ftp.example.com:21,myuser,mypassword,passive,ftps,explicit"
    );
  }

  // Split by comma, but respect %2C in password
  const parts = connStr.split(",");
  if (parts.length < 3) {
    throw new Error(
      "FTP_CONNECTION must have at least 3 fields: host:port,username,password\n" +
      `Got: ${connStr}`
    );
  }

  const hostPort = parts[0].trim();
  const username = parts[1].trim();
  // Decode %2C back to comma in password
  const password = parts[2].trim().replace(/%2C/gi, ",");
  const mode = (parts[3] || "passive").trim().toLowerCase();
  const protocol = (parts[4] || "ftp").trim().toLowerCase();
  const tlsMode = (parts[5] || "").trim().toLowerCase();

  // Parse host and port
  let host, port;
  const lastColon = hostPort.lastIndexOf(":");
  if (lastColon > 0) {
    host = hostPort.substring(0, lastColon);
    port = parseInt(hostPort.substring(lastColon + 1), 10);
    if (isNaN(port)) {
      throw new Error(`Invalid port in host:port — "${hostPort}"`);
    }
  } else {
    host = hostPort;
    port = protocol === "ftps" && tlsMode === "implicit" ? 990 : 21;
  }

  // Determine secure option for basic-ftp
  // false = plain FTP, true = explicit FTPS, "implicit" = implicit FTPS
  let secure = false;
  if (protocol === "ftps") {
    if (tlsMode === "implicit") {
      secure = "implicit";
    } else {
      // explicit (default for ftps)
      secure = true;
    }
  }

  return { host, port, username, password, mode, protocol, tlsMode, secure };
}

/**
 * Create and connect an FTP client using FTP_CONNECTION env var.
 * Returns the connected client instance.
 */
export async function createFtpClient(options = {}) {
  const connStr = process.env.FTP_CONNECTION;
  const config = parseFtpConnection(connStr);

  const client = new Client(options.timeout || 30000);

  if (options.verbose) {
    client.ftp.verbose = true;
  }

  const accessOpts = {
    host: config.host,
    port: config.port,
    user: config.username,
    password: config.password,
    secure: config.secure,
  };

  // For FTPS, allow self-signed certificates by default (common for FTP servers)
  if (config.secure) {
    accessOpts.secureOptions = {
      rejectUnauthorized: false,
    };
  }

  try {
    await client.access(accessOpts);
  } catch (err) {
    client.close();
    throw new Error(
      `Failed to connect to FTP server ${config.host}:${config.port} — ${err.message}`
    );
  }

  return { client, config };
}

/**
 * Parse command line arguments into a simple object.
 */
export function parseArgs(argv) {
  const args = argv.slice(2);
  const result = { _: [] };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--long" || arg === "-l") {
      result.long = true;
    } else if (arg === "--dir" || arg === "-d") {
      result.dir = true;
    } else if (arg === "--verbose" || arg === "-v") {
      result.verbose = true;
    } else if ((arg === "--out" || arg === "-o") && i + 1 < args.length) {
      result.out = args[++i];
    } else if ((arg === "--to" || arg === "-t") && i + 1 < args.length) {
      result.to = args[++i];
    } else if (arg === "--encoding" && i + 1 < args.length) {
      result.encoding = args[++i];
    } else if (arg.startsWith("-")) {
      // Unknown flag, skip
      console.error(`Unknown option: ${arg}`);
    } else {
      result._.push(arg);
    }
  }

  return result;
}

/**
 * Format file size to human-readable string.
 */
export function formatSize(bytes) {
  if (bytes === 0) return "0 B";
  const units = ["B", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return (bytes / Math.pow(1024, i)).toFixed(i > 0 ? 1 : 0) + " " + units[i];
}

/**
 * Format date to readable string.
 */
export function formatDate(date) {
  if (!date) return "N/A";
  return date.toISOString().replace("T", " ").substring(0, 19);
}