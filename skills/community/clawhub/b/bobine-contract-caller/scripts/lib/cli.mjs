export function usageAndExit(message, usage) {
  if (message) console.error(message)
  console.error(usage)
  process.exit(1)
}

export function parseOptions(argv) {
  const options = { params: [] }

  for (let index = 0; index < argv.length; index++) {
    const arg = argv[index]

    if (!arg?.startsWith("--")) {
      usageAndExit(`Unexpected positional argument: ${arg}`, CALL_USAGE)
    }

    const key = arg.slice(2)
    const value = argv[index + 1]

    if (key === "param") {
      if (!value || value.startsWith("--")) {
        usageAndExit("Missing value after --param", CALL_USAGE)
      }

      options.params.push(value)
      index += 1
      continue
    }

    if (!value || value.startsWith("--")) {
      usageAndExit(`Missing value after --${key}`, CALL_USAGE)
    }

    options[key] = value
    index += 1
  }

  return options
}

export const CALL_USAGE = `Call a Bobine contract from one command.

Usage:
  node ./scripts/call_bobine.mjs \\
    --server <bobine-base-url> \\
    --module <target-module> \\
    --method <target-method> \\
    [--param <typed-param>]... \\
    [--auth-module <ed25519-module>] \\
    [--sigkey <private-ed25519-pkcs8-hex>] \\
    [--pubkey <public-ed25519-spki-hex>] \\
    [--spark-effort <target>] \\
    [--spark-hex <single-spark-hex>]

Examples:
  node ./scripts/call_bobine.mjs --server http://localhost:8080 --module <addr> --method get_name
  node ./scripts/call_bobine.mjs --server http://localhost:8080 --module <addr> --method set_name --param text:Alice --auth-module <ed25519> --sigkey <hex> --pubkey <hex>

Rules:
  --server, --module, and --method are always required
  Add --auth-module only for signed Ed25519 calls
  If --auth-module is present, --sigkey and --pubkey are required
  Use either --spark-hex for a one-off provided spark, or --spark-effort to generate one inline
  Repeat --param for each Bobine argument`
