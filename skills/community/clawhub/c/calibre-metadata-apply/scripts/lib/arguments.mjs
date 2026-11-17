export function args(argv, allowed) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith("--")) {
      out._.push(a);
      continue;
    }
    const k = a.slice(2);
    if (!allowed.includes(k) || Object.hasOwn(out, k))
      throw new Error("unknown/duplicate option --" + k);
    if (i + 1 >= argv.length || argv[i + 1].startsWith("--"))
      throw new Error("--" + k + " requires a value");
    out[k] = argv[++i];
  }
  return out;
}
