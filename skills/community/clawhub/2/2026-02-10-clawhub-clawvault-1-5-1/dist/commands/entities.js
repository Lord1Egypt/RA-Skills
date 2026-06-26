import {
  getVaultPath
} from "../chunk-4KDZZW4X.js";
import {
  buildEntityIndex
} from "../chunk-J7ZWCI2C.js";

// src/commands/entities.ts
async function entitiesCommand(options) {
  const vaultPath = getVaultPath();
  const index = buildEntityIndex(vaultPath);
  if (options.json) {
    const output = {};
    for (const [path, entry] of index.byPath) {
      output[path] = entry.aliases;
    }
    console.log(JSON.stringify(output, null, 2));
    return;
  }
  const byFolder = {};
  for (const [path, entry] of index.byPath) {
    const folder = path.split("/")[0];
    if (!byFolder[folder]) byFolder[folder] = [];
    byFolder[folder].push({ path, aliases: entry.aliases });
  }
  console.log("\u{1F4DA} Linkable Entities\n");
  for (const [folder, entities] of Object.entries(byFolder)) {
    console.log(`## ${folder}/`);
    for (const entity of entities) {
      const name = entity.path.split("/")[1];
      const otherAliases = entity.aliases.filter((a) => a.toLowerCase() !== name.toLowerCase());
      if (otherAliases.length > 0) {
        console.log(`  - ${name} (${otherAliases.join(", ")})`);
      } else {
        console.log(`  - ${name}`);
      }
    }
    console.log();
  }
  console.log(`Total: ${index.byPath.size} entities, ${index.entries.size} linkable aliases`);
}
export {
  entitiesCommand
};
