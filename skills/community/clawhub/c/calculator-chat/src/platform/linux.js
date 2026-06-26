const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);
const LAUNCH_DELAY_MS = 800;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function launchCalculator() {
  // Use --solve flag to display number directly (no xdotool needed)
  // This opens calculator with the number shown
  try {
    // Kill any existing calculator first
    try {
      await execAsync('pkill -f gnome-calculator', { stdio: 'ignore' });
    } catch (e) {
      // Ignore if no process running
    }
    await sleep(200);
    
    // Launch with the number - will be handled by typeNumber
    // Just ensure calculator is ready
    await execAsync('gnome-calculator &', { stdio: 'ignore' });
    await sleep(LAUNCH_DELAY_MS);
  } catch (error) {
    console.error('Failed to launch calculator:', error.message);
    throw error;
  }
}

async function typeNumber(number) {
  if (!number) {
    throw new Error('Number parameter is required');
  }

  try {
    // Use --solve flag to directly display the number
    // This works without xdotool!
    await execAsync(`gnome-calculator -s ${number} &`, { stdio: 'ignore' });
    console.log(`Displayed ${number} on calculator`);
  } catch (error) {
    console.error('Failed to type to calculator:', error.message);
    throw error;
  }
}

module.exports = { launchCalculator, typeNumber };
