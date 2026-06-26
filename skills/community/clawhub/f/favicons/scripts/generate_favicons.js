/**
 * Favicons Generator - Generate website icons using the favicons library
 * 
 * Usage:
 *   node generate_favicons.js <source-image-path> <output-directory> [config-JSON]
 * 
 * Example:
 *   node generate_favicons.js ./logo.png ./dist '{"appName":"My App"}'
 */

const { favicons } = require('favicons');
const fs = require('fs').promises;
const path = require('path');

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.error('Usage: node generate_favicons.js <source-image-path> <output-directory> [config-JSON]');
    process.exit(1);
  }

  const source = args[0];
  const dest = args[1];
  const htmlBasename = 'favicon-tags.html';
  
  // Default configuration
  const config = args[2] ? JSON.parse(args[2]) : {};
  
  // Ensure output directory exists
  await fs.mkdir(dest, { recursive: true });

  console.log(`🔍 Source image: ${source}`);
  console.log(`📁 Output directory: ${dest}`);
  console.log('');

  try {
    const response = await favicons(source, {
      path: '/',                        // Path where icons will be stored on the server
      appName: config.appName || null,
      appShortName: config.appShortName || null,
      appDescription: config.appDescription || null,
      developerName: config.developerName || null,
      developerURL: config.developerURL || null,
      background: config.background || '#fff',
      theme_color: config.theme_color || '#fff',
      icons: {
        android: config.android !== undefined ? config.android : true,
        appleIcon: config.appleIcon !== undefined ? config.appleIcon : true,
        appleStartup: config.appleStartup !== undefined ? config.appleStartup : false,
        favicons: config.favicons !== undefined ? config.favicons : true,
        windows: config.windows !== undefined ? config.windows : true,
        yandex: config.yandex !== undefined ? config.yandex : false,
      },
      ...config
    });

    // Save image files
    console.log('🖼️  Generating image files...');
    await Promise.all(
      response.images.map(async (image) => {
        const filePath = path.join(dest, image.name);
        await fs.writeFile(filePath, image.contents);
        console.log(`   ✅ ${image.name}`);
      })
    );

    // Save configuration files
    console.log('\n📄 Generating configuration files...');
    await Promise.all(
      response.files.map(async (file) => {
        const filePath = path.join(dest, file.name);
        await fs.writeFile(filePath, file.contents);
        console.log(`   ✅ ${file.name}`);
      })
    );

    // Save HTML tags
    console.log('\n🏷️  Generating HTML tag file...');
    await fs.writeFile(
      path.join(dest, htmlBasename),
      response.html.join('\n')
    );
    console.log(`   ✅ ${htmlBasename}`);

    // Summary statistics
    console.log('\n📊 Summary statistics:');
    console.log(`   Image files: ${response.images.length}`);
    console.log(`   Configuration files: ${response.files.length}`);
    console.log(`   HTML tags: ${response.html.length}`);

    console.log('\n✅ Icon generation complete!');
    
  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
}

main();