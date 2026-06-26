import React from 'react';
import { cn } from '@/lib/utils';

// Replace ALL occurrences of 'StitchComponent' with your actual component name.
// Example: ProductCard, HeroSection, NavigationBar, KPICard, DataTable
//
// Key patterns in this template:
// - Readonly<T> props interface (required — never use plain interface for props)
// - React.FC<Props> typing
// - cn() for class composition (no hardcoded hex values)
// - Dark mode classes on all color utilities
// - Semantic HTML elements (section, article, nav, button vs div)

interface StitchComponentProps extends Readonly<{
  children?: React.ReactNode;
  className?: string;
  // Add your specific props here — use proper types, no `any`
  // Example:
  // title: string;
  // isActive?: boolean;
  // onClick?: () => void;
}> {}

export const StitchComponent: React.FC<StitchComponentProps> = ({
  children,
  className,
  ...props
}) => {
  return (
    <section
      className={cn(
        // Base styles — use Tailwind theme classes only, no arbitrary hex values
        'relative rounded-lg bg-surface p-4',
        // Dark mode variant
        'dark:bg-surface-dark',
        // Passed-in overrides
        className
      )}
      {...props}
    >
      {children}
    </section>
  );
};

export default StitchComponent;
